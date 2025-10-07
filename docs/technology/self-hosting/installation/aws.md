---
title: Install on Amazon Web Services (AWS)
toc_maxdepth: 2
---

This guide provides an overview of deploying Corridor on Amazon Web Services. Corridor supports three deployment approaches on AWS.

## Overview

### Deployment Options

#### Option 1: Kubernetes - EKS

Deploy Corridor on Amazon Elastic Kubernetes Service (EKS) for a cloud-native, containerized deployment.

**Best for:**
- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

#### Option 2: Serverless - Fargate

Deploy Corridor on AWS Fargate for a serverless container deployment.

**Best for:**
- Organizations wanting minimal infrastructure management
- Predictable workloads
- Cost optimization for variable workloads
- Simplified operations

#### Option 3: Virtual Machines - EC2

Deploy Corridor on Amazon EC2 for a traditional VM-based deployment.

**Best for:**
- Organizations preferring VM-based infrastructure
- Direct control over the operating system
- Traditional IT infrastructure patterns
- Custom hardware requirements

## Common AWS Services

All deployment options utilize these AWS managed services:

- **Amazon RDS**: PostgreSQL database for metadata
- **Amazon S3**: Object storage for file management
- **Elastic Load Balancing**: HTTP(S) load balancing
- **Route 53**: Domain name management
- **VPC**: Virtual private cloud networking

## EKS Installation

### Background

Corridor can be deployed on EKS using Kubernetes to manage containerized services. The deployment leverages AWS's managed services for databases, storage, and networking.

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

#### Optional AWS Services

- **Route 53**: For domain management
- **Secrets Manager**: For storing sensitive configuration
- **CloudWatch**: For logging and monitoring
- **AWS WAF**: For DDoS protection and WAF
- **CloudFront**: For static asset caching

### Architecture Overview

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

### Installation Steps

#### Step 1: Setup EKS Cluster

1. Create EKS cluster
2. Setup NAT Gateway for private cluster internet access
3. Enable cluster autoscaling
4. Configure security groups

#### Step 2: Setup Supporting Infrastructure

1. Create RDS PostgreSQL instance
2. Create EFS filesystem and mount targets
3. Configure VPC networking and security groups

#### Step 3: Install Cluster Components

Install one-time cluster-level components:

1. AWS Load Balancer Controller
2. cert-manager for automated TLS certificates
3. EFS CSI Driver

#### Step 4: Deploy Corridor

1. Create Kubernetes namespace
2. Create database in RDS
3. Configure Kustomize overlay
4. Create container registry pull secrets
5. Apply Kubernetes manifests using Kustomize
6. Configure DNS and verify deployment

### Post Installation

After deployment:

1. **Configure DNS**: Point domain to ALB DNS name
2. **Verify TLS**: Ensure certificates are issued by cert-manager
3. **Create Admin User**: Initialize first admin user account
4. **Test Connectivity**: Verify all services are accessible

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

### EKS-Specific Features

- **Managed Node Groups**: Simplified node management
- **Node Auto-scaling**: Automatic cluster scaling based on workload demands
- **CloudWatch Integration**: Built-in logging and metrics collection
- **IAM Roles for Service Accounts**: Fine-grained pod permissions

### Cost Optimization

- Use **Spot Instances**: For non-production workloads (up to 90% savings)
- Enable **Cluster Autoscaling**: Scale down during off-hours
- Use **Savings Plans**: For predictable production workloads
- Right-size **Node Groups**: Use appropriate instance types for workloads
- Use **S3 Lifecycle Rules**: For backup storage optimization

### Security Best Practices

- Deploy in **private subnets** with NAT Gateway
- Use **IAM Roles for Service Accounts** (IRSA)
- Configure **Security Groups** for pod-to-pod traffic
- Use **Private EKS Clusters** with authorized networks only
- Enable **Control Plane Logging**
- Store secrets in AWS Secrets Manager or Kubernetes secrets

### Example Configurations

### Example Dockerfile

Below is an example Dockerfile for containerizing Corridor applications:

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
# NOTE: Don't use UV_COMPILE_BYTECODE=1 here. It increases the image build time significantly
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#caching
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

**Building the Image:**

```bash
# Build wheel distributions first
uv build --wheel

# Build Docker image with BuildKit
docker build -t corridor/ggx:latest .

# For multi-platform builds
docker buildx build --platform linux/amd64,linux/arm64 -t corridor/ggx:latest .
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

Below is an example Terraform configuration for provisioning AWS infrastructure for Corridor on EKS:

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
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# Public Subnets
resource "aws_subnet" "public" {
  count                   = 3
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 10}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "corridor-public-${count.index + 1}"
    "kubernetes.io/role/elb" = "1"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "corridor-igw"
  }
}

# NAT Gateway
resource "aws_eip" "nat" {
  count  = 3
  domain = "vpc"

  tags = {
    Name = "corridor-nat-${count.index + 1}"
  }
}

resource "aws_nat_gateway" "main" {
  count         = 3
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = {
    Name = "corridor-nat-${count.index + 1}"
  }
}

# Route Tables
resource "aws_route_table" "private" {
  count  = 3
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }

  tags = {
    Name = "corridor-private-rt-${count.index + 1}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "corridor-public-rt"
  }
}

# Route Table Associations
resource "aws_route_table_association" "private" {
  count          = 3
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

resource "aws_route_table_association" "public" {
  count          = 3
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# EKS Cluster
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.28"

  vpc_config {
    subnet_ids              = concat(aws_subnet.private[*].id, aws_subnet.public[*].id)
    endpoint_private_access = true
    endpoint_public_access  = false
  }

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }

  tags = {
    Name = "corridor-eks"
  }
}

# EKS Node Group
resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "corridor-nodes"
  node_role_arn   = aws_iam_role.eks_node_group.arn
  subnet_ids      = aws_subnet.private[*].id

  scaling_config {
    desired_size = 3
    max_size     = 10
    min_size     = 3
  }

  instance_types = ["t3.medium"]

  tags = {
    Name = "corridor-nodes"
  }
}

# RDS Instance
resource "aws_db_instance" "postgres" {
  identifier           = "corridor-db"
  engine              = "postgres"
  engine_version      = "14.9"
  instance_class      = "db.t3.xlarge"
  allocated_storage   = 100
  storage_type        = "gp3"
  storage_encrypted   = true
  
  db_name             = "corridor"
  username           = "corridor"
  password           = var.db_password

  multi_az           = true
  publicly_accessible = false
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

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

## Fargate Installation

### Background

Corridor can be deployed on AWS Fargate using a single service with multiple containers. This deployment leverages AWS's managed services and eliminates the need to manage servers or clusters.

### Prerequisites

- AWS Account with appropriate IAM permissions
- AWS CLI installed and configured
- Access to Corridor container images
- Sufficient AWS service quotas

### Required AWS Services

1. **Amazon ECS**: Container orchestration
   - Fargate launch type
   - Service auto-scaling
   - Application Load Balancer

2. **Amazon RDS**: PostgreSQL database for metadata
   - PostgreSQL 14+ recommended
   - Multi-AZ configuration
   - Automated backups enabled

3. **Amazon EFS**: File storage for persistent data
   - Mount targets in each subnet
   - Access from ECS tasks

### Optional AWS Services

- **Route 53**: For domain management
- **Secrets Manager**: For storing sensitive configuration
- **CloudWatch**: For logging and monitoring
- **AWS WAF**: For DDoS protection and WAF
- **CloudFront**: For static asset caching

### Architecture Overview

```
ECS Cluster (Fargate)
└── Corridor Service
    └── Task Definition
        ├── corridor-app Container (Web UI)
        ├── corridor-worker Container (Celery workers)
        ├── corridor-jupyter Container (JupyterHub)
        └── redis Container (Message Queue)
```

**Key Components:**

- **Single ECS Service**: Running all containers
- **Shared Task Definition**: All components in one task
- **ALB**: HTTP routing and load balancing
- **EFS**: Shared persistent storage

### Installation Steps

#### Step 1: Setup ECS Infrastructure

1. Create VPC with public/private subnets
2. Setup NAT Gateway for private subnet internet access
3. Create ECS cluster
4. Configure security groups

#### Step 2: Setup Supporting Infrastructure

1. Create RDS PostgreSQL instance
2. Create EFS filesystem and mount targets
3. Configure Application Load Balancer
4. Setup IAM roles and execution policies

#### Step 3: Create Task Definition

Create a single task definition containing all containers:
- corridor-app container
- corridor-worker container
- corridor-jupyter container
- redis container

#### Step 4: Deploy Service

1. Create ECS service
2. Configure service discovery
3. Setup ALB target group
4. Configure auto-scaling
5. Setup DNS and verify deployment

### Example Task Definition

```json
{
  "family": "corridor",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "4096",
  "memory": "16384",
  "executionRoleArn": "arn:aws:iam::ACCOUNT_ID:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/corridorTaskRole",
  "containerDefinitions": [
    {
      "name": "corridor-app",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/corridor/ggx:latest",
      "cpu": 2048,
      "memory": 4096,
      "essential": true,
      "command": ["/opt/corridor/venv/bin/corridor-app", "run"],
      "portMappings": [
        {
          "containerPort": 5002,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "WSGI_SERVER",
          "value": "gunicorn"
        }
      ],
      "secrets": [
        {
          "name": "DB_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:corridor/db-password"
        }
      ],
      "mountPoints": [
        {
          "sourceVolume": "corridor-data",
          "containerPath": "/opt/corridor/data",
          "readOnly": false
        }
      ],
      "dependsOn": [
        {
          "containerName": "redis",
          "condition": "START"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/corridor",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "app"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:5002/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    },
    {
      "name": "corridor-worker",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/corridor/ggx:latest",
      "cpu": 1024,
      "memory": 4096,
      "essential": true,
      "command": ["/opt/corridor/venv/bin/corridor-worker", "run"],
      "mountPoints": [
        {
          "sourceVolume": "corridor-data",
          "containerPath": "/opt/corridor/data",
          "readOnly": false
        }
      ],
      "dependsOn": [
        {
          "containerName": "redis",
          "condition": "START"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/corridor",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "worker"
        }
      }
    },
    {
      "name": "corridor-jupyter",
      "image": "ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/corridor/ggx:latest",
      "cpu": 512,
      "memory": 4096,
      "essential": false,
      "command": ["/opt/corridor/venv/bin/corridor-jupyter", "run"],
      "portMappings": [
        {
          "containerPort": 5003,
          "protocol": "tcp"
        }
      ],
      "mountPoints": [
        {
          "sourceVolume": "corridor-data",
          "containerPath": "/opt/corridor/data",
          "readOnly": false
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/corridor",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "jupyter"
        }
      }
    },
    {
      "name": "redis",
      "image": "redis:7-alpine",
      "cpu": 512,
      "memory": 1024,
      "essential": true,
      "portMappings": [
        {
          "containerPort": 6379,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/corridor",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "redis"
        }
      }
    }
  ],
  "volumes": [
    {
      "name": "corridor-data",
      "efsVolumeConfiguration": {
        "fileSystemId": "fs-xxxxxx",
        "transitEncryption": "ENABLED"
      }
    }
  ]
}
```

### Example Service Configuration

```json
{
  "cluster": "corridor",
  "serviceName": "corridor",
  "taskDefinition": "corridor",
  "desiredCount": 2,
  "launchType": "FARGATE",
  "platformVersion": "LATEST",
  "networkConfiguration": {
    "awsvpcConfiguration": {
      "subnets": ["subnet-xxxxx", "subnet-yyyyy"],
      "securityGroups": ["sg-zzzzz"],
      "assignPublicIp": "DISABLED"
    }
  },
  "loadBalancers": [
    {
      "targetGroupArn": "arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:targetgroup/corridor-app/xxxxx",
      "containerName": "corridor-app",
      "containerPort": 5002
    },
    {
      "targetGroupArn": "arn:aws:elasticloadbalancing:REGION:ACCOUNT_ID:targetgroup/corridor-jupyter/yyyyy",
      "containerName": "corridor-jupyter",
      "containerPort": 5003
    }
  ],
  "serviceConnectConfiguration": {
    "enabled": true,
    "namespace": "corridor",
    "services": [
      {
        "portName": "redis",
        "discoveryName": "redis",
        "clientAliases": [
          {
            "port": 6379
          }
        ]
      }
    ]
  },
  "deploymentConfiguration": {
    "deploymentCircuitBreaker": {
      "enable": true,
      "rollback": true
    },
    "maximumPercent": 200,
    "minimumHealthyPercent": 100
  },
  "enableECSManagedTags": true,
  "propagateTags": "SERVICE",
  "enableExecuteCommand": true
}
```

### Cost Optimization

- Use **Fargate Spot**: For non-production workloads (up to 70% savings)
- Enable **Service Auto-scaling**: Scale down during off-hours
- Use **Compute Savings Plans**: For predictable workloads
- Right-size **Task Resources**: Adjust CPU/memory based on usage

### Security Best Practices

- Deploy in **private subnets** with NAT Gateway
- Use **Task IAM Roles** for service permissions
- Configure **Security Groups** for task communication
- Enable **Execute Command** logging
- Store secrets in AWS Secrets Manager
- Enable **Container Insights** for monitoring

## EC2 Installation

### Background

Corridor can be deployed on a single EC2 instance running all components (app, api, workers, jupyter). This approach provides a simple deployment model suitable for organizations that prefer traditional VM-based infrastructure.

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- SSH access to EC2 instance
- Access to Corridor installation bundle
- Sufficient AWS service quotas
- [Minimum Requirements and System Dependencies](./minimum-requirements.md) are met

### Required AWS Services

1. **Amazon EC2**: Virtual machine for running all Corridor components
   - Instance size based on [Minimum Requirements](./minimum-requirements.md)
   - Recommended: t3.2xlarge or larger
   - EBS volume for local storage

2. **Amazon RDS**: PostgreSQL database for metadata
   - PostgreSQL 14+ recommended
   - Multi-AZ configuration (for production)
   - Automated backups enabled

### Optional AWS Services

- **Route 53**: For domain management
- **Secrets Manager**: For storing sensitive configuration
- **CloudWatch**: For logging and monitoring
- **AWS WAF**: For DDoS protection and WAF
- **CloudFront**: For static asset caching

### Architecture Overview

```
EC2 Instance (t3.2xlarge)
├── Corridor Components
│   ├── corridor-app (Web UI)
│   ├── corridor-api (API Server)
│   ├── corridor-worker-api (API Worker)
│   ├── corridor-worker-spark (Spark Worker)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Local Storage
    └── EBS Volume (/opt/corridor)

Amazon RDS
└── PostgreSQL Database
    ├── Metadata
    └── Application Data
```

### Installation Steps

#### Step 1: Launch EC2 Instance

```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0123456789abcdef0 \
  --instance-type t3.2xlarge \
  --key-name your-key \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --block-device-mappings '[
    {
      "DeviceName": "/dev/xvda",
      "Ebs": {
        "VolumeSize": 100,
        "VolumeType": "gp3"
      }
    }
  ]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=corridor-server}]'
```

#### Step 2: Create RDS Instance

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier corridor-db \
  --db-instance-class db.t3.xlarge \
  --engine postgres \
  --engine-version 14.9 \
  --master-username corridor \
  --master-user-password <secure-password> \
  --allocated-storage 100 \
  --storage-type gp3 \
  --multi-az \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name corridor-db-subnet
```

#### Step 3: Install System Dependencies

SSH into the EC2 instance and run:

```bash
# Update system
sudo yum update -y

# Install dependencies
sudo yum install -y \
    python3.11 \
    python3.11-devel \
    java-1.8.0-openjdk \
    redis \
    nginx \
    unzip

# Start and enable Redis
sudo systemctl start redis
sudo systemctl enable redis
```

#### Step 4: Install Corridor Components

1. Extract the installation bundle:
```bash
cd /tmp
unzip corridor-bundle.zip
```

2. Install each component:
```bash
# Install Web Application Server
sudo ./corridor-bundle/install app -i /opt/corridor

# Install API Server
sudo ./corridor-bundle/install api -i /opt/corridor

# Install API Worker
sudo ./corridor-bundle/install worker-api -i /opt/corridor

# Install Spark Worker
sudo ./corridor-bundle/install worker-spark -i /opt/corridor

# Install Jupyter
sudo ./corridor-bundle/install jupyter -i /opt/corridor
```

#### Step 5: Configure Components

1. Update API configuration in `/opt/corridor/instances/default/config/api_config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:password@corridor-db.xxxxx.region.rds.amazonaws.com:5432/corridor"
```

2. Initialize the database:
```bash
/opt/corridor/venv-api/bin/corridor-api db upgrade
```

#### Step 6: Create Service Files

Create systemd service files for each component:

1. Web Application Server (`/etc/systemd/system/corridor-app.service`):
```ini
[Unit]
Description=Corridor Application Server
After=network.target redis.service

[Service]
Type=simple
User=corridor
Group=corridor
Environment=CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
Environment=WSGI_SERVER=gunicorn
ExecStart=/opt/corridor/venv-app/bin/corridor-app run
Restart=always

[Install]
WantedBy=multi-user.target
```

2. API Server (`/etc/systemd/system/corridor-api.service`):
```ini
[Unit]
Description=Corridor API Server
After=network.target redis.service

[Service]
Type=simple
User=corridor
Group=corridor
Environment=CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
Environment=WSGI_SERVER=gunicorn
ExecStart=/opt/corridor/venv-api/bin/corridor-api run
Restart=always

[Install]
WantedBy=multi-user.target
```

3. API Worker (`/etc/systemd/system/corridor-worker-api.service`):
```ini
[Unit]
Description=Corridor API Worker
After=network.target redis.service

[Service]
Type=simple
User=corridor
Group=corridor
Environment=CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
Environment=C_FORCE_ROOT=1
ExecStart=/opt/corridor/venv-api/bin/corridor-worker run --queue api
Restart=always

[Install]
WantedBy=multi-user.target
```

4. Spark Worker (`/etc/systemd/system/corridor-worker-spark.service`):
```ini
[Unit]
Description=Corridor Spark Worker
After=network.target redis.service

[Service]
Type=simple
User=corridor
Group=corridor
Environment=CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
Environment=C_FORCE_ROOT=1
ExecStart=/opt/corridor/venv-api/bin/corridor-worker run --queue spark --queue quick_spark
Restart=always

[Install]
WantedBy=multi-user.target
```

5. Jupyter (`/etc/systemd/system/corridor-jupyter.service`):
```ini
[Unit]
Description=Corridor Jupyter
After=network.target

[Service]
Type=simple
User=corridor
Group=corridor
Environment=CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
ExecStart=/opt/corridor/venv-jupyter/bin/corridor-jupyter run
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Step 7: Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter

# Start services
sudo systemctl start corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter
```

### Service Management

```bash
# Check service status
sudo systemctl status corridor-app
sudo systemctl status corridor-api
sudo systemctl status corridor-worker-api
sudo systemctl status corridor-worker-spark
sudo systemctl status corridor-jupyter
sudo systemctl status redis

# Restart services
sudo systemctl restart corridor-app
sudo systemctl restart corridor-api
sudo systemctl restart corridor-worker-api
sudo systemctl restart corridor-worker-spark
sudo systemctl restart corridor-jupyter
sudo systemctl restart redis
```

### Security Best Practices

- Deploy in **private subnet** with NAT Gateway
- Use **IAM Instance Profile** for AWS service access
- Configure **Security Groups** for instance access
- Enable **Systems Manager Session Manager** for SSH
- Store secrets in AWS Secrets Manager
- Enable **CloudWatch Agent** for monitoring
- Configure **RDS encryption** at rest
- Enable **automated backups** for RDS

### Example Terraform Configuration

```hcl
# EC2 Instance
resource "aws_instance" "corridor" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.2xlarge"
  subnet_id     = aws_subnet.private.id

  root_block_device {
    volume_size = 100
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = file("init.sh")

  tags = {
    Name = "corridor-server"
  }
}

# RDS Instance
resource "aws_db_instance" "corridor" {
  identifier           = "corridor-db"
  engine              = "postgres"
  engine_version      = "14.9"
  instance_class      = "db.t3.xlarge"
  allocated_storage   = 100
  storage_type        = "gp3"
  storage_encrypted   = true
  
  db_name             = "corridor"
  username           = "corridor"
  password           = var.db_password

  multi_az           = true
  publicly_accessible = false
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  deletion_protection = true

  tags = {
    Name = "corridor-db"
  }
}
```