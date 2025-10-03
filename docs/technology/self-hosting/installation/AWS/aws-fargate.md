---
title: Install on AWS - ECS Fargate
---

This guide provides an overview of deploying Corridor on AWS ECS Fargate for a serverless container deployment.

## Background

Corridor can be deployed on AWS Fargate using a single service with multiple containers. This deployment leverages AWS's managed services and eliminates the need to manage servers or clusters.

## Before Installation

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

## Architecture Overview

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

## Installation Overview

### Step 1: Setup ECS Infrastructure

1. Create VPC with public/private subnets
2. Setup NAT Gateway for private subnet internet access
3. Create ECS cluster
4. Configure security groups

### Step 2: Setup Supporting Infrastructure

1. Create RDS PostgreSQL instance
2. Create EFS filesystem and mount targets
3. Configure Application Load Balancer
4. Setup IAM roles and execution policies

### Step 3: Create Task Definition

Create a single task definition containing all containers:
- corridor-app container
- corridor-worker container
- corridor-jupyter container
- redis container

### Step 4: Deploy Service

1. Create ECS service
2. Configure service discovery
3. Setup ALB target group
4. Configure auto-scaling
5. Setup DNS and verify deployment

## Example Task Definition

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

## Example Service Configuration

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

## Monitoring and Operations

### View Logs

```bash
# View all container logs
aws logs tail /ecs/corridor --follow

# View specific container logs
aws logs tail /ecs/corridor --filter-pattern "app"    # corridor-app logs
aws logs tail /ecs/corridor --filter-pattern "worker" # corridor-worker logs
```

### Access Containers

```bash
# Execute command in container
aws ecs execute-command \
  --cluster corridor \
  --task <task-id> \
  --container corridor-app \
  --command "/bin/bash" \
  --interactive
```

### Update Service

```bash
# Update service (new image)
aws ecs update-service \
  --cluster corridor \
  --service corridor \
  --force-new-deployment

# Check deployment status
aws ecs describe-services \
  --cluster corridor \
  --services corridor
```

## Cost Optimization

- Use **Fargate Spot**: For non-production workloads (up to 70% savings)
- Enable **Service Auto-scaling**: Scale down during off-hours
- Use **Compute Savings Plans**: For predictable workloads
- Right-size **Task Resources**: Adjust CPU/memory based on usage

## Security Best Practices

- Deploy in **private subnets** with NAT Gateway
- Use **Task IAM Roles** for service permissions
- Configure **Security Groups** for task communication
- Enable **Execute Command** logging
- Store secrets in AWS Secrets Manager
- Enable **Container Insights** for monitoring

