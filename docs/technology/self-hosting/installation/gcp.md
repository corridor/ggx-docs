---
title: Install on Google Cloud Platform (GCP)
toc_maxdepth: 2
---

This guide provides an overview of deploying Corridor on Google Cloud Platform. Corridor supports two deployment approaches on GCP.

## Overview

### Deployment Options

#### Option 1: Kubernetes - GKE

Deploy Corridor on Google Kubernetes Engine (GKE) for a cloud-native, containerized deployment.

**Best for:**
- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

#### Option 2: Virtual Machines - Compute Engine

Deploy Corridor on Google Compute Engine VMs for a traditional VM-based deployment.

**Best for:**
- Organizations preferring VM-based infrastructure
- Simpler operational model
- Direct control over the operating system
- Traditional IT infrastructure patterns

### Common GCP Services

Both deployment options utilize these GCP managed services:

- **Cloud SQL**: PostgreSQL database for metadata
- **Cloud Storage**: Object storage for file management (or Filestore for NFS)
- **Cloud Load Balancing**: HTTP(S) load balancing
- **Cloud DNS**: Domain name management
- **VPC**: Virtual private cloud networking

## GKE Installation

Corridor can be deployed on GKE using Kubernetes to manage containerized services. The deployment leverages GCP's managed services for databases, storage, and networking.

### Prerequisites

- GCP Project with appropriate permissions
- `gcloud` CLI installed and configured
- `kubectl` CLI installed (via gcloud components)
- Access to Corridor container images
- Sufficient GCP quota for required resources

### Required GCP Services

1. **Google Kubernetes Engine (GKE)**: Managed Kubernetes cluster
   - Private cluster recommended
   - Node autoscaling configured
   - Cloud NAT for egress traffic

2. **Cloud SQL**: PostgreSQL database for metadata
   - PostgreSQL 14+ recommended
   - High availability configuration
   - Automated backups enabled

3. **Google Filestore**: NFS storage for persistent volumes
   - Standard tier: 1TB+ capacity
   - Accessible from GKE cluster VPC

### Optional GCP Services

- **Cloud DNS**: For domain management
- **Secret Manager**: For storing sensitive configuration
- **Cloud Monitoring**: For logging and monitoring
- **Cloud Armor**: For DDoS protection and WAF
- **Cloud CDN**: For static asset caching

### Architecture Overview

```
GKE Cluster
├── Application Namespace
│   ├── corridor-app (Web UI)
│   ├── corridor-worker (Celery workers)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Cluster Components
    ├── NGINX Ingress Controller
    ├── cert-manager (TLS)
    └── NFS Provisioner
```

**Key Components:**

- **Persistent Volumes**: NFS-backed storage via Google Filestore
- **NGINX Ingress**: HTTP routing and load balancing
- **cert-manager**: Automated Let's Encrypt TLS certificates
- **Redis**: Container-based Redis service for message queuing

### Installation Steps

#### Step 1: Setup GKE Cluster

1. Create GKE cluster
2. Setup Cloud NAT for private cluster internet access
3. Enable cluster autoscaling
4. Configure authorized networks for cluster access

#### Step 2: Setup Supporting Infrastructure

1. Create Cloud SQL PostgreSQL instance
2. Create Google Filestore instance for NFS storage
3. Configure VPC networking and firewall rules

#### Step 3: Install Cluster Components

Install one-time cluster-level components:

1. NGINX Ingress Controller
2. cert-manager for automated TLS certificates
3. NFS subdir external provisioner

#### Step 4: Deploy Corridor

1. Create Kubernetes namespace
2. Create database in Cloud SQL
3. Configure Kustomize overlay
4. Create container registry pull secrets
5. Apply Kubernetes manifests using Kustomize
6. Configure DNS and verify deployment

### Post Installation

After deployment:

1. **Configure DNS**: Point domain to Ingress external IP address
2. **Verify TLS**: Ensure certificates are issued by cert-manager (check after 5-10 minutes)
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
# View ingress and external IP
kubectl get ingress -n <namespace>

# Check certificate status
kubectl get certificate -n <namespace>

# View persistent volume claims
kubectl get pvc -n <namespace>
```

### GKE-Specific Features

- **GKE Autopilot** (optional): Fully managed Kubernetes with optimized configurations
- **Node Auto-scaling**: Automatic cluster scaling based on workload demands
- **Cloud Monitoring Integration**: Built-in logging and metrics collection
- **Binary Authorization**: Enforce deployment policies and image attestation

### Cost Optimization

- Use **Preemptible Nodes**: For non-production workloads (up to 80% savings)
- Enable **Cluster Autoscaling**: Scale down during off-hours
- Use **Committed Use Discounts**: For predictable production workloads
- Right-size **Node Pools**: Use appropriate machine types for workloads
- Use **Cloud Storage** lifecycle policies for backups

### Security Best Practices

- Deploy in **private subnets** with Cloud NAT
- Enable **Binary Authorization** for image verification
- Configure **Network Policies** for pod-to-pod traffic
- Use **Private GKE Clusters** with authorized networks only
- Enable **Shielded GKE Nodes** for secure boot
- Store secrets in Kubernetes secrets

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

Below is an example Terraform configuration for provisioning GCP infrastructure for Corridor on GKE:

```hcl
# terraform.tf - Main configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

variable "zone" {
  description = "GCP Zone"
  type        = string
  default     = "us-central1-a"
}

variable "cluster_name" {
  description = "GKE Cluster Name"
  type        = string
  default     = "corridor-gke"
}

# VPC Network
resource "google_compute_network" "vpc" {
  name                    = "corridor-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "corridor-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/16"
  }
}

# Cloud NAT for private cluster
resource "google_compute_router" "router" {
  name    = "corridor-router"
  region  = var.region
  network = google_compute_network.vpc.id
}

resource "google_compute_router_nat" "nat" {
  name                               = "corridor-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

# GKE Cluster
resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.zone

  # Private cluster configuration
  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  # Network configuration
  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Remove default node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  # Maintenance window
  maintenance_policy {
    daily_maintenance_window {
      start_time = "03:00"
    }
  }

  # Add-ons
  addons_config {
    http_load_balancing {
      disabled = false
    }
    horizontal_pod_autoscaling {
      disabled = false
    }
  }
}

# Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = "primary-node-pool"
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = 3

  autoscaling {
    min_node_count = 3
    max_node_count = 10
  }

  node_config {
    machine_type = "n2-standard-4"
    disk_size_gb = 100
    disk_type    = "pd-standard"

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }
}

# Cloud SQL Instance
resource "google_sql_database_instance" "postgres" {
  name             = "corridor-db"
  database_version = "POSTGRES_14"
  region           = var.region

  settings {
    tier              = "db-custom-4-16384"
    availability_type = "REGIONAL"
    disk_size         = 100
    disk_type         = "PD_SSD"

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled    = true
      private_network = google_compute_network.vpc.id
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "corridor_db"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "user" {
  name     = "corridor"
  instance = google_sql_database_instance.postgres.name
  password = var.db_password # Store in terraform.tfvars or use Secret Manager
}

# Filestore Instance
resource "google_filestore_instance" "nfs" {
  name     = "corridor-nfs"
  location = var.zone
  tier     = "STANDARD"

  file_shares {
    capacity_gb = 1024
    name        = "corridor"
  }

  networks {
    network = google_compute_network.vpc.name
    modes   = ["MODE_IPV4"]
  }
}

# Outputs
output "cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}

output "cluster_endpoint" {
  value       = google_container_cluster.primary.endpoint
  description = "GKE Cluster Endpoint"
  sensitive   = true
}

output "cloudsql_connection_name" {
  value       = google_sql_database_instance.postgres.connection_name
  description = "Cloud SQL Connection Name"
}

output "filestore_ip" {
  value       = google_filestore_instance.nfs.networks[0].ip_addresses[0]
  description = "Filestore NFS IP Address"
}
```

**Usage:**

```bash
# Initialize Terraform
terraform init

# Create terraform.tfvars file
cat > terraform.tfvars <<EOF
project_id = "your-gcp-project-id"
region     = "us-central1"
zone       = "us-central1-a"
db_password = "secure-password-here"
EOF

# Plan the deployment
terraform plan

# Apply the configuration
terraform apply

# Get kubectl credentials
gcloud container clusters get-credentials corridor-gke \
  --zone us-central1-a \
  --project your-gcp-project-id
```

**Notes:**
- Store sensitive variables in `terraform.tfvars` (add to `.gitignore`)
- Consider using Terraform Cloud or GCS backend for remote state
- Adjust machine types and disk sizes based on your requirements
- Review and customize network policies and firewall rules

## VM Installation

### Background

Corridor can be deployed on a single GCE instance running all components (app, api, workers, jupyter). This approach provides a simple deployment model suitable for organizations that prefer traditional VM-based infrastructure.

### Prerequisites

- GCP Project with appropriate permissions
- `gcloud` CLI installed and configured
- SSH access to GCE instance
- Access to Corridor installation bundle
- Sufficient GCP service quotas
- [Minimum Requirements and System Dependencies](./minimum-requirements.md) are met

### Required GCP Services

1. **Compute Engine**: VM for running all Corridor components
   - Instance size based on [Minimum Requirements](./minimum-requirements.md)
   - Recommended: n2-standard-8 or larger
   - Persistent SSD for local storage

2. **Cloud SQL**: PostgreSQL database for metadata
   - PostgreSQL 14+ recommended
   - High availability configuration
   - Automated backups enabled

### Optional GCP Services

- **Cloud DNS**: For domain management
- **Secret Manager**: For storing sensitive configuration
- **Cloud Monitoring**: For logging and monitoring
- **Cloud Armor**: For DDoS protection and WAF
- **Cloud CDN**: For static asset caching

### Architecture Overview

```
GCE Instance (n2-standard-8)
├── Corridor Components
│   ├── corridor-app (Web UI)
│   ├── corridor-api (API Server)
│   ├── corridor-worker-api (API Worker)
│   ├── corridor-worker-spark (Spark Worker)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Local Storage
    └── Persistent SSD (/opt/corridor)

Cloud SQL
└── PostgreSQL Database
    ├── Metadata
    └── Application Data
```

### Installation Steps

#### Step 1: Create GCE Instance

```bash
# Create instance
gcloud compute instances create corridor-vm \
  --machine-type=n2-standard-8 \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=100GB \
  --boot-disk-type=pd-ssd \
  --create-disk=name=corridor-data,size=100GB,type=pd-ssd \
  --network=default \
  --subnet=default \
  --zone=us-central1-a

# Create Cloud SQL instance
gcloud sql instances create corridor-db \
  --database-version=POSTGRES_14 \
  --cpu=4 \
  --memory=16GB \
  --region=us-central1 \
  --availability-type=REGIONAL \
  --storage-type=SSD \
  --storage-size=100GB \
  --backup \
  --backup-start-time=03:00
```

#### Step 2: Install System Dependencies

SSH into the GCE instance and run:

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

#### Step 3: Install Corridor Components

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

#### Step 4: Configure Components

1. Update API configuration in `/opt/corridor/instances/default/config/api_config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:password@<INSTANCE_IP>:5432/corridor"
```

2. Initialize the database:
```bash
/opt/corridor/venv-api/bin/corridor-api db upgrade
```

#### Step 5: Create Service Files

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

#### Step 6: Start Services

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

- Deploy in **private subnet** with Cloud NAT
- Use **Service Accounts** for GCP service access
- Configure **Firewall Rules** for instance access
- Enable **OS Login** for SSH access
- Store secrets in Secret Manager
- Enable **Cloud Monitoring Agent** for monitoring
- Configure **Cloud SQL encryption** at rest
- Enable **automated backups** for Cloud SQL

### Example Terraform Configuration

```hcl
# GCE Instance
resource "google_compute_instance" "corridor" {
  name         = "corridor-vm"
  machine_type = "n2-standard-8"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size  = 100
      type  = "pd-ssd"
    }
  }

  attached_disk {
    source = google_compute_disk.data.self_link
  }

  network_interface {
    network = "default"
    subnetwork = "default"
  }

  service_account {
    scopes = ["cloud-platform"]
  }

  metadata = {
    startup-script = file("init.sh")
  }

  tags = {
    Name = "corridor-server"
  }
}

# Persistent Disk
resource "google_compute_disk" "data" {
  name  = "corridor-data"
  type  = "pd-ssd"
  zone  = "us-central1-a"
  size  = 100
}

# Cloud SQL Instance
resource "google_sql_database_instance" "corridor" {
  name             = "corridor-db"
  database_version = "POSTGRES_14"
  region           = "us-central1"

  settings {
    tier              = "db-custom-4-16384"
    availability_type = "REGIONAL"
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled    = true
      private_network = google_compute_network.vpc.id
    }

    disk_size = 100
    disk_type = "PD_SSD"
  }

  deletion_protection = true
}

resource "google_sql_database" "corridor" {
  name     = "corridor"
  instance = google_sql_database_instance.corridor.name
}

resource "google_sql_user" "corridor" {
  name     = "corridor"
  instance = google_sql_database_instance.corridor.name
  password = var.db_password
}
```