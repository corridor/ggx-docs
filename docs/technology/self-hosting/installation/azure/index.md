---
title: Install on Microsoft Azure
---

This guide provides an overview of deploying Corridor on Microsoft Azure. Corridor supports two deployment approaches on Azure.

## Deployment Options

### Option 1: Kubernetes - AKS

Deploy Corridor on Azure Kubernetes Service (AKS) for a cloud-native, containerized deployment.

**Best for:**

- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

[View AKS Installation Guide →](./azure-aks.md)

### Option 2: Virtual Machines - Azure VMs

Deploy Corridor on Azure Virtual Machines for a traditional VM-based deployment.

**Best for:**

- Organizations preferring VM-based infrastructure
- Direct control over the operating system
- Traditional IT infrastructure patterns
- Custom hardware requirements

[View Azure VMs Installation Guide →](./azure-vms.md)

## Common Azure Services

Both deployment options utilize these Azure managed services:

- **Azure Database for PostgreSQL**: Metadata storage
- **Azure Storage**: Object storage for file management (or Azure Files for NFS)
- **Application Gateway**: HTTP(S) load balancing
- **Azure DNS**: Domain name management
- **Virtual Network**: Private cloud networking

## Choosing the Right Option

| Factor | AKS (Kubernetes) | Azure VMs |
|--------|------------------|-----------|
| **Complexity** | Higher | Lower |
| **Scalability** | Automatic | Manual |
| **Multi-tenancy** | Native (namespaces) | Separate VMs |
| **Operational Overhead** | Lower (managed K8s) | Higher |
| **Deployment Speed** | Faster | Moderate |
| **Infrastructure Management** | Minimal | Full |
| **Cost Model** | Node-based | Per instance |
| **Kubernetes Skills Required** | Yes | No |