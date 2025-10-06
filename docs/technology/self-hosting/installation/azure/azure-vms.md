---
title: Install on Azure - Virtual Machines
---

This guide provides an overview of deploying Corridor on a single Azure Virtual Machine.

## Background

Corridor can be deployed on a single Azure VM running all components (app, api, workers, jupyter). This approach provides a simple deployment model suitable for organizations that prefer traditional VM-based infrastructure.

## Before Installation

### Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed and configured
- SSH access to Azure VM
- Access to Corridor installation bundle
- Sufficient Azure service quotas
- [Minimum Requirements and System Dependencies](../minimum-requirements.md) are met

### Required Azure Services

1. **Azure Virtual Machines**: VM for running all Corridor components
   - Instance size based on [Minimum Requirements](../minimum-requirements.md)
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

## Architecture Overview

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

## Installation Steps

### Step 1: Create Azure VM

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

### Step 2: Create PostgreSQL Database

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

### Step 3: Install System Dependencies

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

### Step 4: Install Corridor Components

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

### Step 5: Configure Components

1. Update API configuration in `/opt/corridor/instances/default/config/api_config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:password@corridor-db.postgres.database.azure.com:5432/corridor"
```

2. Initialize the database:
```bash
/opt/corridor/venv-api/bin/corridor-api db upgrade
```

### Step 6: Create Service Files

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

### Step 7: Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter

# Start services
sudo systemctl start corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter
```

## Monitoring and Operations


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

## Security Best Practices

- Deploy in **private subnet** with NAT Gateway
- Use **Managed Identities** for Azure service access
- Configure **Network Security Groups** for VM access
- Enable **Azure Bastion** for SSH access
- Store secrets in Azure Key Vault
- Enable **Azure Monitor Agent** for monitoring
- Configure **PostgreSQL encryption** at rest
- Enable **automated backups** for PostgreSQL

## Example Terraform Configuration

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