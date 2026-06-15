---
title: "Terraform"
---

Use Terraform when you want Corridor infrastructure provisioned as code on a supported cloud. Corridor maintains cloud-specific Terraform repositories for managed container deployments:

- [`corridor/terraform-aws-ggx`](https://github.com/corridor/terraform-aws-ggx) for AWS ECS Fargate.
- [`corridor/terraform-azurerm-ggx`](https://github.com/corridor/terraform-azurerm-ggx) for Azure Container Apps.
- [`corridor/terraform-google-ggx`](https://github.com/corridor/terraform-google-ggx) for Google Cloud Run.

These modules are separate from the [Kubernetes](../kubernetes/) manifests. Use Kubernetes for AKS, GKE, or EKS clusters. Use Terraform when you want cloud-managed container services and the surrounding cloud infrastructure created through IaC.

## Common Workflow

Each repository follows the same Terraform workflow:

```bash
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with cloud, image, database, hostname, and license values.
terraform init
terraform plan
terraform apply
```

Keep `terraform.tfvars` and state files out of source control unless your organization has an approved secrets and backend workflow. For production, configure a remote backend such as S3, Azure Storage, or GCS and restrict state access because state may contain sensitive values.

## AWS Module

The AWS module runs Corridor on ECS Fargate. It provisions or configures:

- One ECS service on an ECS cluster.
- A Fargate task definition with `corridor-migration`, `redis`, `corridor-app`, `corridor-worker`, and `corridor-jupyter`.
- Application Load Balancer routing `/` to the app container and `/jupyter` to Jupyter.
- EFS file system, mount targets, and access points for shared persistent state.
- IAM task execution and task roles.
- CloudWatch log group.
- Security groups for ALB, ECS tasks, and EFS.

Primary configuration values include:

- `image`
- `hostname`
- `certificate_arn`
- `database_url`
- `license_key`

See the [AWS](../aws/) page for AWS service and permission guidance.

## Azure Module

The Azure module deploys Corridor on Azure Container Apps. It provisions or configures:

- Container Apps for the app, worker, Jupyter, Redis, PostgreSQL-facing configuration, and Nginx routing.
- Azure Files for shared storage.
- Optional dedicated workload profiles when the default consumption profile is not enough.
- Resource group, Container App Environment, storage account, and database-related outputs.

Primary configuration values include:

- `resource_group_name`
- `location`
- `acr_login_server`
- `acr_sp_client_id`
- `acr_sp_client_secret`
- `image_name`
- `image_version`
- `corridor_license_key`
- `db_admin_password`
- `app_workload_profile`

See the [Azure](../azure/) page for Azure service and permission guidance.

## Google Cloud Module

The Google Cloud module runs Corridor on Cloud Run and maps the Kubernetes application shape to managed Google Cloud services. It provisions or configures:

- `corridor-migration` as a Cloud Run Job.
- `corridor-app`, `corridor-worker`, and `corridor-jupyter` as Cloud Run services.
- Cloud SQL for PostgreSQL.
- Memorystore for Redis.
- Cloud Storage for shared file-backed state.
- Direct VPC egress for private service connectivity.
- External HTTPS load balancer with serverless NEGs so `/` routes to the app and `/jupyter` routes to Jupyter.
- Service account and IAM bindings.

Primary configuration values include:

- `project_id`
- `image`
- `hostname`
- `db_password`
- `license_key`
- SMTP values when email notifications are required

See the [GCP](../gcp/) page for Google Cloud service and permission guidance.

## When To Use Terraform

| Requirement | Recommended path |
|---|---|
| Managed Kubernetes on AKS, GKE, or EKS | [Kubernetes](../kubernetes/) |
| AWS serverless containers | Terraform AWS ECS Fargate module |
| Azure managed containers | Terraform Azure Container Apps module |
| Google Cloud managed containers | Terraform Cloud Run module |
| Existing VMs or bare metal | [Manual](../manual/) |
| Existing Docker host or compose environment | [Docker-based](../docker-based/) |
