---
title: "AWS"
---

Use this page to choose and configure an AWS deployment path for GGX.

## Recommended AWS Paths

| Path | Use when | Primary docs |
|---|---|---|
| EKS | You already operate Kubernetes or need namespace isolation and Kubernetes-native operations | [Kubernetes](../kubernetes/) |
| ECS Fargate | You want AWS-managed containers without managing Kubernetes nodes | [Terraform](../terraform/) |
| EC2 or other VMs | You want a traditional VM-based install and direct OS control | [Manual](../manual/) |

## EKS-Specific Configuration

EKS uses the shared [GGX Kubernetes manifests](https://github.com/corridor/kubernetes-ggx). Start with the [Kubernetes](../kubernetes/) page, then apply the AWS-specific requirements below.

### Required AWS Services

- **Amazon EKS** for the managed Kubernetes cluster.
- **Amazon RDS for PostgreSQL** for GGX metadata.
- **Amazon EFS** for read-write-many persistent volumes.
- **Application Load Balancer** through AWS Load Balancer Controller.
- **Amazon VPC** with private subnets for workloads and controlled public ingress.
- **IAM** for cluster roles, controller permissions, and workload identities.

Optional but common services:

- **Route 53** for DNS.
- **AWS Certificate Manager** for TLS certificates.
- **Secrets Manager** for sensitive configuration.
- **CloudWatch** for logs, metrics, and alarms.
- **AWS WAF** for edge protection.

### Permissions

The deploying role or CI identity needs permission to manage:

- EKS clusters and managed node groups.
- VPCs, subnets, route tables, NAT Gateways, and security groups.
- IAM roles, policies, and IAM Roles for Service Accounts (IRSA).
- EFS file systems, mount targets, and access points.
- RDS instances, subnet groups, and security groups.
- ALB listeners, target groups, and ingress-related resources.
- Route 53 records and ACM certificates when DNS and TLS are managed in AWS.

### Cluster Add-ons

Install or enable these before applying the GGX overlay:

- AWS Load Balancer Controller for ALB-backed ingress.
- EFS CSI Driver for persistent volumes.
- cert-manager if TLS is issued by Kubernetes.
- Cluster Autoscaler or Karpenter for node scaling.
- CloudWatch Container Insights or another approved observability stack.

### Networking

Production EKS deployments should normally use private worker nodes with outbound internet access through NAT. Security groups must allow:

- ALB to reach the GGX app and Jupyter services.
- GGX pods to reach RDS PostgreSQL.
- GGX pods to reach EFS mount targets.
- Pods to pull GGX images from the configured registry.

## ECS Fargate With Terraform

The [GGX AWS Terraform module](https://github.com/corridor/terraform-aws-ggx) deploys GGX on ECS Fargate. This is the main non-Kubernetes AWS path.

The Fargate deployment uses:

- A single ECS service with a task definition containing `corridor-migration`, `corridor-app`, `corridor-worker`, and `corridor-jupyter`.
- Application Load Balancer routing `/` to `corridor-app` on port `5002`.
- Application Load Balancer routing `/jupyter` to `corridor-jupyter` on port `5003`.
- EFS for shared persistent storage.
- CloudWatch logs.
- IAM task execution and task roles.

Configure the module with the GGX image, hostname, ACM certificate ARN, database URL, and license key. Then run:

```bash
terraform init
terraform plan
terraform apply
```

Useful ECS operations:

```bash
aws logs tail /ecs/corridor --follow
aws ecs update-service --cluster corridor --service corridor --force-new-deployment
aws ecs describe-services --cluster corridor --services corridor
```

## EC2 Or VM-Based Installs

An EC2 deployment follows the [Manual](../manual/) path. The EC2 installation pattern is:

1. Launch an EC2 instance sized from the [minimum requirements](../minimum-requirements/), commonly `t3.2xlarge` or larger for all-in-one deployments.
2. Create an RDS PostgreSQL database.
3. Install system dependencies such as Python 3.11, Java 8 for Spark, Nginx, and unzip.
4. Extract the GGX installation bundle.
5. Install the `app`, `api`, `worker-api`, `worker-spark`, and `jupyter` components.
6. Configure `/opt/corridor/instances/default/config/api_config.py`.
7. Run `corridor-api db upgrade`.
8. Create systemd services and start the components.

Use EC2 when you need direct host access or your organization standardizes on VM operations. Use EKS or ECS Fargate when you want managed container operations.

## Security Notes

- Do not deploy with the AWS account root user.
- Store application secrets in Secrets Manager or an approved secret store.
- Use private subnets for application workloads and databases.
- Enable encryption at rest for RDS and EFS.
- Use least-privilege IAM roles for controllers, tasks, and operations.
- Enable CloudWatch logs and billing alerts before production rollout.
