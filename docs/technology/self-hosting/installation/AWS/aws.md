---
title: Install on Amazon Web Services (AWS)
---

This guide provides an overview of deploying Corridor on Amazon Web Services. Corridor supports three deployment approaches on AWS.

## Deployment Options

### Option 1: Kubernetes - EKS

Deploy Corridor on Amazon Elastic Kubernetes Service (EKS) for a cloud-native, containerized deployment.

**Best for:**

- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

[View EKS Installation Guide →](./aws-eks.md)

### Option 2: Serverless - ECS Fargate

Deploy Corridor using AWS Fargate for a serverless container deployment.

**Best for:**

- Organizations wanting serverless infrastructure
- Minimal infrastructure management
- Variable workload patterns

[View Fargate Installation Guide →](./aws-fargate.md)

### Option 3: Virtual Machines - EC2

Deploy Corridor on Amazon EC2 instances for a traditional VM-based deployment.

**Best for:**

- Organizations preferring VM-based infrastructure
- Direct control over the operating system
- Traditional IT infrastructure patterns
- Custom hardware requirements

[View EC2 Installation Guide →](./aws-ec2.md)

## Common AWS Services

All deployment options utilize these AWS managed services:

- **RDS**: PostgreSQL database for metadata storage
- **S3**: Object storage for file management (or EFS for NFS)
- **Application Load Balancer**: HTTP(S) load balancing
- **Route 53**: Domain name management
- **VPC**: Virtual private cloud networking

## Choosing the Right Option

| Factor | EKS (Kubernetes) | ECS Fargate | EC2 (VMs) |
|--------|------------------|-------------|------------|
| **Complexity** | Higher | Medium | Lower |
| **Scalability** | Automatic | Automatic | Manual |
| **Multi-tenancy** | Native (namespaces) | Task-based | Separate VMs |
| **Operational Overhead** | Lower (managed K8s) | Lowest | Higher |
| **Deployment Speed** | Fast | Fastest | Moderate |
| **Infrastructure Management** | Minimal | None | Full |
| **Cost Model** | Node-based | Per task | Per instance |
| **Kubernetes Skills Required** | Yes | No | No |