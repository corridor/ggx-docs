---
title: Install on Microsoft Azure
toc_maxdepth: 2
---

This guide provides an overview of deploying Corridor on Microsoft Azure. Corridor supports two deployment approaches on Azure.

## Overview

### Deployment Options

#### Option 1: Kubernetes - AKS

Deploy Corridor on Azure Kubernetes Service (AKS) for a cloud-native, containerized deployment.

**Best for:**
- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

#### Option 2: Virtual Machines

Deploy Corridor on Azure Virtual Machines for a traditional VM-based deployment.

**Best for:**
- Organizations preferring VM-based infrastructure
- Direct control over the operating system
- Traditional IT infrastructure patterns
- Custom hardware requirements

## Common Azure Services

Both deployment options utilize these Azure managed services:

- **Azure Database for PostgreSQL**: Database for metadata
- **Azure Storage**: Blob storage for file management
- **Azure Load Balancer**: HTTP(S) load balancing
- **Azure DNS**: Domain name management
- **Virtual Network**: Private cloud networking

## AKS Installation

### Background

Corridor can be deployed on AKS using Kubernetes to manage containerized services. The deployment leverages Azure's managed services for databases, storage, and networking.

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

### Architecture Overview

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

### Installation Steps

#### Step 1: Setup AKS Cluster

1. Create AKS cluster
2. Configure virtual network
3. Enable cluster autoscaling
4. Configure authorized networks

#### Step 2: Setup Supporting Infrastructure

1. Create Azure Database for PostgreSQL
2. Create Azure Files share
3. Configure networking and firewall rules

#### Step 3: Install Cluster Components

Install one-time cluster-level components:

1. NGINX Ingress Controller
2. cert-manager for automated TLS certificates
3. Azure Files CSI Driver

#### Step 4: Deploy Corridor

1. Create Kubernetes namespace
2. Create database in Azure PostgreSQL
3. Configure Kustomize overlay
4. Create container registry pull secrets
5. Apply Kubernetes manifests using Kustomize
6. Configure DNS and verify deployment

### Post Installation

After deployment:

1. **Configure DNS**: Point domain to Ingress IP address
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
# View ingress and IP
kubectl get ingress -n <namespace>

# Check certificate status
kubectl get certificate -n <namespace>

# View persistent volume claims
kubectl get pvc -n <namespace>
```

### AKS-Specific Features

- **Managed Node Pools**: Simplified node management
- **Virtual Node**: Serverless container hosting with ACI
- **Azure Monitor Integration**: Built-in logging and metrics
- **Azure AD Integration**: Identity and RBAC

### Cost Optimization

- Use **Spot Node Pools**: For non-production workloads (up to 90% savings)
- Enable **Cluster Autoscaling**: Scale down during off-hours
- Use **Reserved Instances**: For predictable workloads
- Right-size **Node Pools**: Use appropriate VM sizes
- Use **Storage Lifecycle**: For backup storage optimization

### Security Best Practices

- Deploy in **private subnets**
- Use **Managed Identities** for service authentication
- Configure **Network Policies** for pod-to-pod traffic
- Use **Private AKS Clusters** with authorized networks
- Enable **Azure Policy** for Kubernetes
- Store secrets in Azure Key Vault

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

### Example Terraform Configuration

Below is an example Terraform configuration for provisioning Azure infrastructure for Corridor on AKS:

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
  dns_prefix          = "corridor-aks"
  kubernetes_version  = "1.28"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D4s_v3"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    service_cidr   = "10.1.0.0/16"
    dns_service_ip = "10.1.0.10"
  }

  tags = {
    Name = "corridor-aks"
  }
}

# PostgreSQL Server
resource "azurerm_postgresql_server" "main" {
  name                = "corridor-db"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  version             = "14"
  sku_name            = "GP_Gen5_4"

  administrator_login          = "corridor"
  administrator_login_password = var.db_password

  backup_retention_days        = 7
  geo_redundant_backup_enabled = true
  auto_grow_enabled           = true

  ssl_enforcement_enabled = true

  tags = {
    Name = "corridor-db"
  }
}

resource "azurerm_postgresql_database" "main" {
  name                = "corridor"
  resource_group_name = azurerm_resource_group.main.name
  server_name         = azurerm_postgresql_server.main.name
  charset             = "UTF8"
  collation           = "English_United States.1252"
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "corridorstorage"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
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

## VM Installation

### Background

Corridor can be deployed on a single Azure VM running all components (app, api, workers, jupyter). This approach provides a simple deployment model suitable for organizations that prefer traditional VM-based infrastructure.

### Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed and configured
- SSH access to Azure VM
- Access to Corridor installation bundle
- Sufficient Azure service quotas
- [Minimum Requirements and System Dependencies](./minimum-requirements.md) are met

### Required Azure Services

1. **Azure Virtual Machines**: VM for running all Corridor components
   - Instance size based on [Minimum Requirements](./minimum-requirements.md)
   - Recommended: Standard_D8s_v3 or larger
   - Premium SSD for local storage

2. **Azure Database for PostgreSQL**: Database for metadata
   - PostgreSQL 14+ recommended
   - Zone redundant configuration (for production)
   - Automated backups enabled

### Optional Azure Services

- **Azure DNS**: For domain management
- **Key Vault**: For storing sensitive configuration
- **Azure Monitor**: For logging and monitoring
- **Application Gateway**: For WAF and load balancing
- **Azure CDN**: For static asset caching

### Architecture Overview

```
Azure VM (Standard_D8s_v3)
├── Corridor Components
│   ├── corridor-app (Web UI)
│   ├── corridor-api (API Server)
│   ├── corridor-worker-api (API Worker)
│   ├── corridor-worker-spark (Spark Worker)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Local Storage
    └── Premium SSD (/opt/corridor)

Azure Database for PostgreSQL
└── PostgreSQL Database
    ├── Metadata
    └── Application Data
```

### Installation Steps

#### Step 1: Create Azure VM

```bash
# Create resource group
az group create \
  --name corridor-rg \
  --location eastus

# Create VM
az vm create \
  --resource-group corridor-rg \
  --name corridor-vm \
  --image UbuntuLTS \
  --size Standard_D8s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --data-disk-sizes-gb 100

# Configure data disk
az vm disk attach \
  --resource-group corridor-rg \
  --vm-name corridor-vm \
  --name corridor-data \
  --size-gb 100 \
  --sku Premium_LRS \
  --new
```

#### Step 2: Create PostgreSQL Database

```bash
# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group corridor-rg \
  --name corridor-db \
  --location eastus \
  --admin-user corridor \
  --admin-password <secure-password> \
  --sku-name Standard_D4s_v3 \
  --tier GeneralPurpose \
  --storage-size 128 \
  --version 14 \
  --high-availability ZoneRedundant
```

#### Step 3: Install System Dependencies

SSH into the Azure VM and run:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y \
    python3.11 \
    python3.11-dev \
    openjdk-8-jdk \
    redis-server \
    nginx \
    unzip

# Start and enable Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
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
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:password@corridor-db.postgres.database.azure.com:5432/corridor"
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
After=network.target redis-server.service

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
After=network.target redis-server.service

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
After=network.target redis-server.service

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
After=network.target redis-server.service

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
sudo systemctl status redis-server

# Restart services
sudo systemctl restart corridor-app
sudo systemctl restart corridor-api
sudo systemctl restart corridor-worker-api
sudo systemctl restart corridor-worker-spark
sudo systemctl restart corridor-jupyter
sudo systemctl restart redis-server
```

### Security Best Practices

- Deploy in **private subnet** with NAT Gateway
- Use **Managed Identities** for Azure service access
- Configure **Network Security Groups** for VM access
- Enable **Azure Bastion** for SSH access
- Store secrets in Azure Key Vault
- Enable **Azure Monitor Agent** for monitoring
- Configure **PostgreSQL encryption** at rest
- Enable **automated backups** for PostgreSQL

### Example Terraform Configuration

```hcl
# Azure VM
resource "azurerm_virtual_machine" "corridor" {
  name                  = "corridor-vm"
  location              = azurerm_resource_group.main.location
  resource_group_name   = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.main.id]
  vm_size              = "Standard_D8s_v3"

  storage_os_disk {
    name              = "corridor-os"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Premium_LRS"
  }

  storage_data_disk {
    name              = "corridor-data"
    managed_disk_type = "Premium_LRS"
    create_option     = "Empty"
    lun               = 0
    disk_size_gb      = 100
  }

  os_profile {
    computer_name  = "corridor"
    admin_username = "azureuser"
  }

  os_profile_linux_config {
    disable_password_authentication = true
    ssh_keys {
      path     = "/home/azureuser/.ssh/authorized_keys"
      key_data = var.ssh_public_key
    }
  }

  tags = {
    Name = "corridor-server"
  }
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server" "corridor" {
  name                = "corridor-db"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  version            = "14"
  
  administrator_login    = "corridor"
  administrator_password = var.db_password

  sku_name = "Standard_D4s_v3"
  
  storage_mb = 131072
  
  zone_redundant = true
  
  backup_retention_days = 7
  
  high_availability {
    mode = "ZoneRedundant"
  }

  maintenance_window {
    day_of_week  = 0
    start_hour   = 3
    start_minute = 0
  }

  tags = {
    Name = "corridor-db"
  }
}
```