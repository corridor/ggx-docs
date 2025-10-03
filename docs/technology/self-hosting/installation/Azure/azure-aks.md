---
title: Install on Azure - Kubernetes (AKS)
---

This guide provides an overview of deploying Corridor on Azure Kubernetes Service (AKS).

## Background

Corridor can be deployed on AKS using Kubernetes to manage containerized services. The deployment leverages Azure's managed services for databases, storage, and networking.

## Before Installation

### Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed and configured
- `kubectl` CLI installed
- Access to Corridor container images
- Sufficient Azure resource quotas

### Required Azure Services

1. **Azure Kubernetes Service (AKS)**: Managed Kubernetes cluster
   - Private cluster recommended
   - Node autoscaling configured
   - Azure CNI networking

2. **Azure Database for PostgreSQL**: Metadata database
   - PostgreSQL 14+ recommended
   - Zone redundant configuration
   - Automated backups enabled

3. **Azure Files Premium**: Storage for persistent volumes
   - Premium tier for performance
   - Access from AKS cluster

### Optional Azure Services

- **Azure DNS**: For domain management
- **Key Vault**: For storing sensitive configuration
- **Azure Monitor**: For logging and monitoring
- **Azure Front Door**: For DDoS protection and WAF
- **Azure CDN**: For static asset caching

## Architecture Overview

```
AKS Cluster
├── Application Namespace
│   ├── corridor-app (Web UI)
│   ├── corridor-worker (Celery workers)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Cluster Components
    ├── NGINX Ingress Controller
    ├── cert-manager (TLS)
    └── CSI Storage Drivers
```

**Key Components:**

- **Persistent Volumes**: Azure Files storage
- **NGINX Ingress**: HTTP routing and load balancing
- **cert-manager**: Automated Let's Encrypt TLS certificates
- **Redis**: Container-based Redis service for message queuing

## Installation Overview

### Step 1: Setup AKS Cluster

1. Create AKS cluster
2. Configure virtual network
3. Enable cluster autoscaling
4. Configure authorized networks

### Step 2: Setup Supporting Infrastructure

1. Create Azure Database for PostgreSQL
2. Create Azure Files share
3. Configure networking and firewall rules

### Step 3: Install Cluster Components

Install one-time cluster-level components:

1. NGINX Ingress Controller
2. cert-manager for automated TLS certificates
3. Azure Files CSI Driver

### Step 4: Deploy Corridor

1. Create Kubernetes namespace
2. Create database in Azure PostgreSQL
3. Configure Kustomize overlay
4. Create container registry pull secrets
5. Apply Kubernetes manifests using Kustomize
6. Configure DNS and verify deployment

## Installation Steps

Contact Corridor support for:

- Complete AKS cluster creation scripts
- Terraform/Infrastructure-as-Code templates
- Kubernetes manifests and Kustomize overlays
- Client deployment configuration examples

## Post Installation

After deployment:

1. **Configure DNS**: Point domain to Ingress IP address
2. **Verify TLS**: Ensure certificates are issued by cert-manager
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
# View ingress and IP
kubectl get ingress -n <namespace>

# Check certificate status
kubectl get certificate -n <namespace>

# View persistent volume claims
kubectl get pvc -n <namespace>
```

## AKS-Specific Features

- **Managed Node Pools**: Simplified node management
- **Virtual Node**: Serverless container hosting with ACI
- **Azure Monitor Integration**: Built-in logging and metrics
- **Azure AD Integration**: Identity and RBAC

## Cost Optimization

- Use **Spot Node Pools**: For non-production workloads (up to 90% savings)
- Enable **Cluster Autoscaling**: Scale down during off-hours
- Use **Reserved Instances**: For predictable workloads
- Right-size **Node Pools**: Use appropriate VM sizes
- Use **Storage Lifecycle**: For backup storage optimization

## Security Best Practices

- Deploy in **private subnets**
- Use **Managed Identities** for service authentication
- Configure **Network Policies** for pod-to-pod traffic
- Use **Private AKS Clusters** with authorized networks
- Enable **Azure Policy** for Kubernetes
- Store secrets in Azure Key Vault

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

### Example Terraform Configuration

```hcl
# terraform.tf - Main configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "corridor-rg"
  location = var.location
}

# Virtual Network
resource "azurerm_virtual_network" "main" {
  name                = "corridor-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "main" {
  name                = "corridor-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = "corridor"

  default_node_pool {
    name                = "default"
    node_count          = 3
    vm_size            = "Standard_D4s_v3"
    enable_auto_scaling = true
    min_count          = 3
    max_count          = 10
    vnet_subnet_id     = azurerm_subnet.aks.id
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "calico"
  }

  private_cluster_enabled = true

  addon_profile {
    oms_agent {
      enabled = true
    }
  }
}

# PostgreSQL Server
resource "azurerm_postgresql_server" "main" {
  name                = "corridor-db"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  sku_name = "GP_Gen5_4"

  storage_mb                   = 102400
  backup_retention_days        = 7
  geo_redundant_backup_enabled = true
  auto_grow_enabled           = true

  administrator_login          = "corridor"
  administrator_login_password = var.db_password
  version                     = "14"
  ssl_enforcement_enabled     = true
}

resource "azurerm_postgresql_database" "main" {
  name                = "corridor"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_postgresql_server.main.name
  charset             = "UTF8"
  collation          = "English_United States.1252"
}

# Azure Files Share
resource "azurerm_storage_account" "main" {
  name                     = "corridorstorage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Premium"
  account_replication_type = "LRS"
  account_kind            = "FileStorage"
}

resource "azurerm_storage_share" "main" {
  name                 = "corridor"
  storage_account_name = azurerm_storage_account.main.name
  quota                = 1024
}

# Outputs
output "aks_name" {
  value       = azurerm_kubernetes_cluster.main.name
  description = "AKS Cluster Name"
}

output "postgresql_fqdn" {
  value       = azurerm_postgresql_server.main.fqdn
  description = "PostgreSQL Server FQDN"
}

output "storage_account_name" {
  value       = azurerm_storage_account.main.name
  description = "Storage Account Name"
}
```

**Usage:**

```bash
# Initialize Terraform
terraform init

# Create terraform.tfvars file
cat > terraform.tfvars <<EOF
location = "eastus"
db_password = "secure-password-here"
EOF

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply

# Get kubectl credentials
az aks get-credentials --resource-group corridor-rg --name corridor-aks
```
