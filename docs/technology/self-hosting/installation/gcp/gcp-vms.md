---
title: Install on GCP - Virtual Machines
---

This guide provides an overview of deploying Corridor on a single Google Compute Engine (GCE) instance.

## Background

Corridor can be deployed on a single GCE instance running all components (app, api, workers, jupyter). This approach provides a simple deployment model suitable for organizations that prefer traditional VM-based infrastructure.

## Before Installation

### Prerequisites

- GCP Project with appropriate permissions
- `gcloud` CLI installed and configured
- SSH access to GCE instance
- Access to Corridor installation bundle
- Sufficient GCP service quotas
- [Minimum Requirements and System Dependencies](../minimum-requirements.md) are met

### Required GCP Services

1. **Compute Engine**: VM for running all Corridor components
   - Instance size based on [Minimum Requirements](../minimum-requirements.md)
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

## Architecture Overview

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

## Installation Steps

### Step 1: Create GCE Instance

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

### Step 2: Install System Dependencies

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

### Step 3: Install Corridor Components

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

### Step 4: Configure Components

1. Update API configuration in `/opt/corridor/instances/default/config/api_config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:password@<INSTANCE_IP>:5432/corridor"
```

2. Initialize the database:
```bash
/opt/corridor/venv-api/bin/corridor-api db upgrade
```

### Step 5: Create Service Files

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

### Step 6: Start Services

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

- Deploy in **private subnet** with Cloud NAT
- Use **Service Accounts** for GCP service access
- Configure **Firewall Rules** for instance access
- Enable **OS Login** for SSH access
- Store secrets in Secret Manager
- Enable **Cloud Monitoring Agent** for monitoring
- Configure **Cloud SQL encryption** at rest
- Enable **automated backups** for Cloud SQL

## Example Terraform Configuration

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