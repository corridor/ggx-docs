---
title: Install on AWS - EC2
---

This guide provides an overview of deploying Corridor on a single Amazon EC2 instance.

## Background

Corridor can be deployed on a single EC2 instance running all components (app, api, workers, jupyter). This approach provides a simple deployment model suitable for organizations that prefer traditional VM-based infrastructure.

## Before Installation

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- SSH access to EC2 instance
- Access to Corridor installation bundle
- Sufficient AWS service quotas
- [Minimum Requirements and System Dependencies](../minimum-requirements.md) are met

### Required AWS Services

1. **Amazon EC2**: Virtual machine for running all Corridor components

   - Instance size based on [Minimum Requirements](../minimum-requirements.md)
   - Recommended: t3.2xlarge or larger
   - EBS volume for local storage

2. **Amazon RDS**: PostgreSQL database for metadata
   - PostgreSQL 14+ recommended
   - Multi-AZ configuration (for production)
   - Automated backups enabled

### Optional AWS Services

- **Route 53**: For domain management
- **Secrets Manager**: For storing sensitive configuration
- **CloudWatch**: For logging and monitoring
- **AWS WAF**: For DDoS protection and WAF
- **CloudFront**: For static asset caching

## Architecture Overview

```
EC2 Instance (t3.2xlarge)
├── Corridor Components
│   ├── corridor-app (Web UI)
│   ├── corridor-api (API Server)
│   ├── corridor-worker-api (API Worker)
│   ├── corridor-worker-spark (Spark Worker)
│   ├── corridor-jupyter (JupyterHub)
│   └── redis (Message Queue)
└── Local Storage
    └── EBS Volume (/opt/corridor)

Amazon RDS
└── PostgreSQL Database
    ├── Metadata
    └── Application Data
```

## Installation Steps

### Step 1: Launch EC2 Instance

```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0123456789abcdef0 \
  --instance-type t3.2xlarge \
  --key-name your-key \
  --security-group-ids sg-xxxxx \
  --subnet-id subnet-xxxxx \
  --block-device-mappings '[
    {
      "DeviceName": "/dev/xvda",
      "Ebs": {
        "VolumeSize": 100,
        "VolumeType": "gp3"
      }
    }
  ]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=corridor-server}]'
```

### Step 2: Create RDS Instance

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier corridor-db \
  --db-instance-class db.t3.xlarge \
  --engine postgres \
  --engine-version 14.9 \
  --master-username corridor \
  --master-user-password <secure-password> \
  --allocated-storage 100 \
  --storage-type gp3 \
  --multi-az \
  --vpc-security-group-ids sg-xxxxx \
  --db-subnet-group-name corridor-db-subnet
```

### Step 3: Install System Dependencies

SSH into the EC2 instance and run:

```bash
# Update system
sudo yum update -y

# Install dependencies
sudo yum install -y \
    python3.11 \
    python3.11-devel \
    java-1.8.0-openjdk \
    redis \
    nginx \
    unzip

# Start and enable Redis
sudo systemctl start redis
sudo systemctl enable redis
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
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:password@corridor-db.xxxxx.region.rds.amazonaws.com:5432/corridor"
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
After=network.target redis.service

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
After=network.target redis.service

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
After=network.target redis.service

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
After=network.target redis.service

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
sudo systemctl status redis

# Restart services
sudo systemctl restart corridor-app
sudo systemctl restart corridor-api
sudo systemctl restart corridor-worker-api
sudo systemctl restart corridor-worker-spark
sudo systemctl restart corridor-jupyter
sudo systemctl restart redis
```

## Security Best Practices

- Deploy in **private subnet** with NAT Gateway
- Use **IAM Instance Profile** for AWS service access
- Configure **Security Groups** for instance access
- Enable **Systems Manager Session Manager** for SSH
- Store secrets in AWS Secrets Manager
- Enable **CloudWatch Agent** for monitoring
- Configure **RDS encryption** at rest
- Enable **automated backups** for RDS

## Example Terraform Configuration

```hcl
# EC2 Instance
resource "aws_instance" "corridor" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.2xlarge"
  subnet_id     = aws_subnet.private.id

  root_block_device {
    volume_size = 100
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = file("init.sh")

  tags = {
    Name = "corridor-server"
  }
}

# RDS Instance
resource "aws_db_instance" "corridor" {
  identifier           = "corridor-db"
  engine              = "postgres"
  engine_version      = "14.9"
  instance_class      = "db.t3.xlarge"
  allocated_storage   = 100
  storage_type        = "gp3"
  storage_encrypted   = true

  db_name             = "corridor"
  username           = "corridor"
  password           = var.db_password

  multi_az           = true
  publicly_accessible = false

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  deletion_protection = true

  tags = {
    Name = "corridor-db"
  }
}
```
