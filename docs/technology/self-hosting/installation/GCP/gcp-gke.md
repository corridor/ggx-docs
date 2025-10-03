---
title: Install on GCP - Kubernetes (GKE)
---

This guide provides an overview of deploying Corridor on Google Kubernetes Engine (GKE).

## Background

Corridor can be deployed on GKE using Kubernetes to manage containerized services. The deployment leverages GCP's managed services for databases, storage, and networking.

## Before Installation

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

## Architecture Overview

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

## Installation Overview

### Step 1: Setup GKE Cluster

1. Create GKE cluster
2. Setup Cloud NAT for private cluster internet access
3. Enable cluster autoscaling
4. Configure authorized networks for cluster access

### Step 2: Setup Supporting Infrastructure

1. Create Cloud SQL PostgreSQL instance
2. Create Google Filestore instance for NFS storage
3. Configure VPC networking and firewall rules

### Step 3: Install Cluster Components

Install one-time cluster-level components:

1. NGINX Ingress Controller
2. cert-manager for automated TLS certificates
3. NFS subdir external provisioner

### Step 4: Deploy Corridor

1. Create Kubernetes namespace
2. Create database in Cloud SQL
3. Configure Kustomize overlay
4. Create container registry pull secrets
5. Apply Kubernetes manifests using Kustomize
6. Configure DNS and verify deployment

## Installation Steps

Contact Corridor support for:

- Complete GKE cluster creation scripts
- Terraform/Infrastructure-as-Code templates
- Kubernetes manifests and Kustomize overlays
- Client deployment configuration examples

## Post Installation

After deployment:

1. **Configure DNS**: Point domain to Ingress external IP address
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
# View ingress and external IP
kubectl get ingress -n <namespace>

# Check certificate status
kubectl get certificate -n <namespace>

# View persistent volume claims
kubectl get pvc -n <namespace>
```

## GKE-Specific Features

- **GKE Autopilot** (optional): Fully managed Kubernetes with optimized configurations
- **Node Auto-scaling**: Automatic cluster scaling based on workload demands
- **Cloud Monitoring Integration**: Built-in logging and metrics collection
- **Binary Authorization**: Enforce deployment policies and image attestation

## Cost Optimization

- Use **Preemptible Nodes**: For non-production workloads (up to 80% savings)
- Enable **Cluster Autoscaling**: Scale down during off-hours
- Use **Committed Use Discounts**: For predictable production workloads
- Right-size **Node Pools**: Use appropriate machine types for workloads
- Use **Cloud Storage** lifecycle policies for backups

## Security Best Practices

- Deploy in **private subnets** with Cloud NAT
- Enable **Binary Authorization** for image verification
- Configure **Network Policies** for pod-to-pod traffic
- Use **Private GKE Clusters** with authorized networks only
- Enable **Shielded GKE Nodes** for secure boot
- Store secrets in Kubernetes secrets

## Example Configurations

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
