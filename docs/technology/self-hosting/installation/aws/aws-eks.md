---
title: Install on AWS - Kubernetes (EKS)
---

This guide provides an overview of deploying Corridor on Amazon Elastic Kubernetes Service (EKS).

## Background

Corridor can be deployed on EKS using Kubernetes to manage containerized services. The deployment leverages AWS's managed services for databases, storage, and networking.

## Before Installation

### Prerequisites

- AWS Account with appropriate IAM permissions
- AWS CLI installed and configured
- `kubectl` CLI installed
- `eksctl` CLI installed
- Access to Corridor container images
- Sufficient AWS service quotas

### Required AWS Services

1. **Amazon EKS**: Managed Kubernetes cluster
   - Private cluster recommended
   - Node autoscaling configured
   - NAT Gateway for egress traffic

2. **Amazon RDS**: PostgreSQL database for metadata
   - PostgreSQL 14+ recommended
   - Multi-AZ configuration
   - Automated backups enabled

3. **Amazon EFS**: NFS storage for persistent volumes
   - Standard tier
   - Mount targets in each subnet
   - Access from EKS cluster VPC

### Optional AWS Services

- **Route 53**: For domain management
- **Secrets Manager**: For storing sensitive configuration
- **CloudWatch**: For logging and monitoring
- **AWS WAF**: For DDoS protection and WAF
- **CloudFront**: For static asset caching

## Architecture Overview

```
EKS Cluster
├── Application Namespace
│   ├── corridor-app (Web UI)
│   ├── corridor-worker (Celery workers)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Cluster Components
    ├── AWS Load Balancer Controller
    ├── cert-manager (TLS)
    └── EFS CSI Driver
```

**Key Components:**

- **Persistent Volumes**: EFS-backed storage
- **ALB Ingress**: HTTP routing and load balancing
- **cert-manager**: Automated Let's Encrypt TLS certificates
- **Redis**: Container-based Redis service for message queuing

## Installation Overview

### Step 1: Setup EKS Cluster

1. Create EKS cluster
2. Setup NAT Gateway for private cluster internet access
3. Enable cluster autoscaling
4. Configure security groups

### Step 2: Setup Supporting Infrastructure

1. Create RDS PostgreSQL instance
2. Create EFS filesystem and mount targets
3. Configure VPC networking and security groups

### Step 3: Install Cluster Components

Install one-time cluster-level components:

1. AWS Load Balancer Controller
2. cert-manager for automated TLS certificates
3. EFS CSI Driver

### Step 4: Deploy Corridor

1. Create Kubernetes namespace
2. Create database in RDS
3. Configure Kustomize overlay
4. Create container registry pull secrets
5. Apply Kubernetes manifests using Kustomize
6. Configure DNS and verify deployment

## Installation Steps

Contact Corridor support for:

- Complete EKS cluster creation scripts
- Terraform/Infrastructure-as-Code templates
- Kubernetes manifests and Kustomize overlays
- Client deployment configuration examples

## Post Installation

After deployment:

1. **Configure DNS**: Point domain to ALB DNS name
2. **Verify TLS**: Ensure certificates are issued by cert-manager (check after 5-10 minutes)
3. **Create Admin User**: Initialize first admin user account
4. **Test Connectivity**: Verify all services are accessible

## Monitoring and Operations

### View Logs

```bash
# View application logs
kubectl logs -n <namespace> deploy/corridor-app

# View worker logs  
kubectl logs -n <namespace> deploy/corridor-worker
```

### Access Services

```bash
# Access pod shell
kubectl exec -it -n <namespace> deploy/corridor-app -- /bin/bash

# View pod status
kubectl get pods -n <namespace>

# View all resources in namespace
kubectl get all -n <namespace>
```

### Update Deployment

```bash
# Restart deployment (pull latest image)
kubectl rollout restart deployment corridor-app -n <namespace>

# Check rollout status
kubectl rollout status deployment corridor-app -n <namespace>
```

### Common Operations

```bash
# View ingress and ALB
kubectl get ingress -n <namespace>

# Check certificate status
kubectl get certificate -n <namespace>

# View persistent volume claims
kubectl get pvc -n <namespace>
```

## EKS-Specific Features

- **Managed Node Groups**: Simplified node management
- **Node Auto-scaling**: Automatic cluster scaling based on workload demands
- **CloudWatch Integration**: Built-in logging and metrics collection
- **IAM Roles for Service Accounts**: Fine-grained pod permissions

## Cost Optimization

- Use **Spot Instances**: For non-production workloads (up to 90% savings)
- Enable **Cluster Autoscaling**: Scale down during off-hours
- Use **Savings Plans**: For predictable production workloads
- Right-size **Node Groups**: Use appropriate instance types for workloads
- Use **S3 Lifecycle Rules**: For backup storage optimization

## Security Best Practices

- Deploy in **private subnets** with NAT Gateway
- Use **IAM Roles for Service Accounts** (IRSA)
- Configure **Security Groups** for pod-to-pod traffic
- Use **Private EKS Clusters** with authorized networks only
- Enable **Control Plane Logging**
- Store secrets in AWS Secrets Manager or Kubernetes secrets

## Example Configurations

### Example Dockerfile

```dockerfile
FROM redhat/ubi8

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV CORRIDOR_HOME=/opt/corridor
# Disable buffering in python to enable faster logging
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN yum update -y \
    && yum install java-1.8.0-openjdk procps-ng https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm -y \
    && yum clean all

# Setup JAVA_HOME so Spark can find the java-1.8.0
ENV JAVA_HOME=/etc/alternatives/jre

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_LINK_MODE=copy

WORKDIR $CORRIDOR_HOME
ENV PATH="/opt/corridor/venv/bin/:$PATH"

COPY uv.lock pyproject.toml $CORRIDOR_HOME/

# Install runtime dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv $CORRIDOR_HOME/venv --python 3.11 --seed \
    && source $CORRIDOR_HOME/venv/bin/activate \
    && uv sync --active --frozen --no-install-workspace --no-group dev --no-group test --extra pyspark

# Install corridor packages
RUN --mount=target=/corridor_wheels,type=bind,source=corridor_wheels \
    uv pip install --python $CORRIDOR_HOME/venv --no-cache-dir /corridor_wheels/*.whl

# Expose application ports
EXPOSE 5002 5003

# Health check (adjust for specific service)
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5002/corr-api || exit 1
```

**Using Different Services:**

The same image can run different Corridor services by overriding the command:

```yaml
# corridor-app
command: ["/opt/corridor/venv/bin/corridor-app", "run"]

# corridor-worker
command: ["/opt/corridor/venv/bin/corridor-worker", "run"]

# corridor-jupyter
command: ["/opt/corridor/venv/bin/corridor-jupyter", "run"]
```

### Example Terraform Configuration

```hcl
# terraform.tf - Main configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# Variables
variable "region" {
  description = "AWS Region"
  type        = string
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "EKS Cluster Name"
  type        = string
  default     = "corridor-eks"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "corridor-vpc"
  }
}

# Private Subnets
resource "aws_subnet" "private" {
  count             = 3
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "corridor-private-${count.index + 1}"
  }
}

# NAT Gateway
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "corridor-nat"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster.arn

  vpc_config {
    subnet_ids              = aws_subnet.private[*].id
    endpoint_private_access = true
    endpoint_public_access  = false
  }

  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
}

# Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "corridor-nodes"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = 3
    min_size     = 3
    max_size     = 10
  }

  instance_types = ["m5.xlarge"]

  tags = {
    Name = "corridor-node-group"
  }
}

# RDS Instance
resource "aws_db_instance" "postgres" {
  identifier           = "corridor-db"
  engine              = "postgres"
  engine_version      = "14"
  instance_class      = "db.t3.xlarge"
  allocated_storage   = 100
  storage_type        = "gp3"
  multi_az           = true
  db_name             = "corridor"
  username           = "corridor"
  password           = var.db_password

  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  deletion_protection = true

  tags = {
    Name = "corridor-db"
  }
}

# EFS Filesystem
resource "aws_efs_file_system" "main" {
  creation_token = "corridor-efs"
  encrypted      = true

  tags = {
    Name = "corridor-efs"
  }
}

resource "aws_efs_mount_target" "main" {
  count           = length(aws_subnet.private)
  file_system_id  = aws_efs_file_system.main.id
  subnet_id       = aws_subnet.private[count.index].id
  security_groups = [aws_security_group.efs.id]
}

# Outputs
output "cluster_endpoint" {
  value       = aws_eks_cluster.main.endpoint
  description = "EKS Cluster Endpoint"
  sensitive   = true
}

output "cluster_name" {
  value       = aws_eks_cluster.main.name
  description = "EKS Cluster Name"
}

output "rds_endpoint" {
  value       = aws_db_instance.postgres.endpoint
  description = "RDS Instance Endpoint"
}

output "efs_id" {
  value       = aws_efs_file_system.main.id
  description = "EFS Filesystem ID"
}
```

**Usage:**

```bash
# Initialize Terraform
terraform init

# Create terraform.tfvars file
cat > terraform.tfvars <<EOF
region = "us-west-2"
db_password = "secure-password-here"
EOF

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply

# Get kubectl credentials
aws eks update-kubeconfig --name corridor-eks --region us-west-2
```

