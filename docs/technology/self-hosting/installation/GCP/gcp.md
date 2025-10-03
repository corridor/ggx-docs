---
title: Install on Google Cloud Platform (GCP)
---

This guide provides an overview of deploying Corridor on Google Cloud Platform. Corridor supports two deployment approaches on GCP.

## Deployment Options

### Option 1: Kubernetes - GKE

Deploy Corridor on Google Kubernetes Engine (GKE) for a cloud-native, containerized deployment.

**Best for:**

- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

[View GKE Installation Guide →](./gcp-gke.md)

### Option 2: Virtual Machines - Compute Engine

Deploy Corridor on Google Compute Engine VMs for a traditional VM-based deployment.

**Best for:**

- Organizations preferring VM-based infrastructure
- Simpler operational model
- Direct control over the operating system
- Traditional IT infrastructure patterns

[View VM Installation Guide →](./gcp-vms.md)

## Common GCP Services

Both deployment options utilize these GCP managed services:

- **Cloud SQL**: PostgreSQL database for metadata storage
- **Cloud Memorystore**: Redis for message queuing
- **Cloud Storage**: Object storage for file management (or Filestore for NFS)
- **Cloud Load Balancing**: HTTP(S) load balancing
- **Cloud DNS**: Domain name management
- **VPC**: Virtual private cloud networking

## Choosing the Right Option

| Factor | GKE (Kubernetes) | VMs (Compute Engine) |
|--------|------------------|----------------------|
| **Complexity** | Higher | Lower |
| **Scalability** | Automatic | Manual |
| **Multi-tenancy** | Native (namespaces) | Separate VMs |
| **Operational Overhead** | Lower (managed K8s) | Higher (OS management) |
| **Deployment Speed** | Faster | Moderate |


