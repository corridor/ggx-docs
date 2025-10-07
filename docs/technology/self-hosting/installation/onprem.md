---
title: Install On-Premises
toc_maxdepth: 2
---

This guide provides an overview of deploying Corridor on-premises or in your own data center infrastructure.

## Overview

### Deployment Options

#### Option 1: Bare Metal / Virtual Machines

Deploy Corridor directly on physical servers or virtual machines using the installation bundle.

**Best for:**

- Organizations with existing VM infrastructure
- Traditional IT infrastructure patterns
- Direct control over the operating system
- Simpler operational model without containers

#### Option 2: Docker Containers

Deploy Corridor using Docker containers for a containerized deployment.

**Best for:**

- Organizations using Docker/container infrastructure
- Simplified deployment and updates
- Resource isolation
- Modern infrastructure patterns

### Common Requirements

Both deployment options require:

- **Metadata Database**: PostgreSQL, Oracle, or SQL Server
- **Message Queue**: Redis for Celery task orchestration
- **File Storage**: Network-attached storage (NAS) or local storage
- **Web Server**: Nginx or Apache (for production)
- **Process Management**: Systemd or Supervisor
- **SSL Certificates**: For HTTPS access

### Choosing the Right Option

| Factor | VMs (Bundle Install) | Docker Containers |
|--------|---------------------|-------------------|
| **Complexity** | Lower | Moderate |
| **Updates** | Manual reinstall | Image replacement |
| **Isolation** | Process-level | Container-level |
| **Resource Usage** | Direct | Slight overhead |
| **Portability** | OS-dependent | OS-independent |
| **Rollback** | Manual | Easy (previous image) |

## Architecture Overview

### VM-Based Architecture

```
On-Premises Infrastructure
├── App Server VM(s)
│   └── corridor-app (Web UI)
├── Worker VM(s)
│   ├── corridor-worker (API worker)
│   └── corridor-worker (Spark worker)
├── Jupyter VM(s)
│   └── corridor-jupyter
├── Database Server (PostgreSQL/Oracle/SQL Server)
├── Redis Server
└── NAS/File Server
```

### Docker-Based Architecture

```
Docker Infrastructure
├── corridor-app (Container)
├── corridor-worker-api (Container)
├── corridor-worker-spark (Container)
├── corridor-jupyter (Container)
├── Database (Container or External)
├── Redis (Container or External)
└── Shared Volumes (Docker Volumes or NAS)
```

## VM Installation

### Prerequisites

- Linux server (Ubuntu 20.04+, RHEL 8+, or CentOS 8+)
- Root or sudo access
- Network connectivity between servers
- Access to Corridor installation bundle
- [Minimum Requirements and System Dependencies](./minimum-requirements.md) are met

### Required Components

1. **Application Server**: Web UI and API
   - RAM: 4 GB minimum
   - CPU: 4 cores minimum
   - Storage: 20 GB minimum
   - Python 3.11+

2. **Worker Server**: Background task processing
   - RAM: 16 GB minimum
   - CPU: 8 cores minimum
   - Storage: 500 GB minimum (for Spark data)
   - Python 3.11+, Java 8+, Spark 3.3+

3. **Jupyter Server**: Interactive notebooks
   - RAM: 4 GB minimum
   - CPU: 4 cores minimum
   - Storage: 10 GB minimum
   - Python 3.11+, Spark 3.3+

4. **Database Server**: Metadata storage
   - RAM: 2 GB minimum
   - CPU: 2 cores minimum
   - Storage: 5 GB minimum
   - PostgreSQL 11.7+, Oracle 19+, or SQL Server 2016+

5. **Redis Server**: Message queue
   - RAM: 1 GB minimum
   - CPU: 1 core minimum
   - Storage: 10 GB minimum
   - Redis 4+

### Installation Steps

#### Step 1: Install System Dependencies

On each server, install the required dependencies:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-dev python3.11-venv

# Install Java 8 (for Spark)
sudo apt-get install -y openjdk-8-jdk

# Install other dependencies
sudo apt-get install -y \
    redis-server \
    nginx \
    unzip \
    curl \
    wget

# Start and enable Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

#### Step 2: Install Corridor Components

1. Extract the installation bundle:
```bash
cd /tmp
unzip corridor-bundle.zip
```

2. Install each component on the appropriate server:

**Application Server:**
```bash
# Install Web Application Server
sudo ./corridor-bundle/install app -i /opt/corridor

# Install API Server
sudo ./corridor-bundle/install api -i /opt/corridor
```

**Worker Server:**
```bash
# Install API Worker
sudo ./corridor-bundle/install worker-api -i /opt/corridor

# Install Spark Worker
sudo ./corridor-bundle/install worker-spark -i /opt/corridor
```

**Jupyter Server:**
```bash
# Install Jupyter
sudo ./corridor-bundle/install jupyter -i /opt/corridor
```

#### Step 3: Configure Database

1. Install and configure PostgreSQL:
```bash
# Install PostgreSQL
sudo apt-get install -y postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql <<EOF
CREATE DATABASE corridor;
CREATE USER corridor WITH PASSWORD 'secure-password';
GRANT ALL PRIVILEGES ON DATABASE corridor TO corridor;
\q
EOF
```

2. Initialize the database:
```bash
/opt/corridor/venv-api/bin/corridor-api db upgrade
```

#### Step 4: Configure Components

1. Update API configuration in `/opt/corridor/instances/default/config/api_config.py`:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://corridor:secure-password@database-server:5432/corridor"
REDIS_URL = "redis://redis-server:6379/0"
```

2. Configure file storage paths in `/opt/corridor/instances/default/config/app_config.py`:
```python
CORRIDOR_DATA_DIR = "/shared/corridor/data"
CORRIDOR_UPLOAD_DIR = "/shared/corridor/uploads"
```

#### Step 5: Create Service Files

Create systemd service files for each component:

**Application Server (`/etc/systemd/system/corridor-app.service`):**
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

**API Server (`/etc/systemd/system/corridor-api.service`):**
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

**API Worker (`/etc/systemd/system/corridor-worker-api.service`):**
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

**Spark Worker (`/etc/systemd/system/corridor-worker-spark.service`):**
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

**Jupyter (`/etc/systemd/system/corridor-jupyter.service`):**
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

#### Step 6: Configure Nginx

Create Nginx configuration for the application server:

```nginx
server {
    listen 80;
    server_name corridor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Step 7: Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable services
sudo systemctl enable corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter

# Start services
sudo systemctl start corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Service Management

```bash
# Check service status
sudo systemctl status corridor-app
sudo systemctl status corridor-api
sudo systemctl status corridor-worker-api
sudo systemctl status corridor-worker-spark
sudo systemctl status corridor-jupyter

# Restart services
sudo systemctl restart corridor-app
sudo systemctl restart corridor-api
sudo systemctl restart corridor-worker-api
sudo systemctl restart corridor-worker-spark
sudo systemctl restart corridor-jupyter
```

## Docker Installation

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Access to Corridor container images
- Network connectivity between containers
- Shared storage accessible to all containers

### Installation Steps

#### Step 1: Create Docker Compose Configuration

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  corridor-app:
    image: corridor/ggx:latest
    command: ["/opt/corridor/venv/bin/corridor-app", "run"]
    ports:
      - "5002:5002"
    environment:
      - CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
      - WSGI_SERVER=gunicorn
    volumes:
      - corridor-data:/opt/corridor/data
      - corridor-config:/opt/corridor/instances/default/config
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  corridor-api:
    image: corridor/ggx:latest
    command: ["/opt/corridor/venv/bin/corridor-api", "run"]
    ports:
      - "5003:5003"
    environment:
      - CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
      - WSGI_SERVER=gunicorn
    volumes:
      - corridor-data:/opt/corridor/data
      - corridor-config:/opt/corridor/instances/default/config
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  corridor-worker-api:
    image: corridor/ggx:latest
    command: ["/opt/corridor/venv/bin/corridor-worker", "run", "--queue", "api"]
    environment:
      - CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
      - C_FORCE_ROOT=1
    volumes:
      - corridor-data:/opt/corridor/data
      - corridor-config:/opt/corridor/instances/default/config
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  corridor-worker-spark:
    image: corridor/ggx:latest
    command: ["/opt/corridor/venv/bin/corridor-worker", "run", "--queue", "spark", "--queue", "quick_spark"]
    environment:
      - CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
      - C_FORCE_ROOT=1
    volumes:
      - corridor-data:/opt/corridor/data
      - corridor-config:/opt/corridor/instances/default/config
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  corridor-jupyter:
    image: corridor/ggx:latest
    command: ["/opt/corridor/venv/bin/corridor-jupyter", "run"]
    ports:
      - "5004:5004"
    environment:
      - CORRIDOR_CONFIG_DIR=/opt/corridor/instances/default/config
    volumes:
      - corridor-data:/opt/corridor/data
      - corridor-config:/opt/corridor/instances/default/config
    depends_on:
      - redis
      - postgres
    restart: unless-stopped

  postgres:
    image: postgres:14
    environment:
      - POSTGRES_DB=corridor
      - POSTGRES_USER=corridor
      - POSTGRES_PASSWORD=secure-password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    restart: unless-stopped

volumes:
  corridor-data:
  corridor-config:
  postgres-data:
  redis-data:
```

#### Step 2: Create Environment Configuration

Create `.env` file:

```bash
# Database Configuration
POSTGRES_DB=corridor
POSTGRES_USER=corridor
POSTGRES_PASSWORD=secure-password

# Redis Configuration
REDIS_URL=redis://redis:6379/0

# Corridor Configuration
CORRIDOR_DATA_DIR=/opt/corridor/data
CORRIDOR_UPLOAD_DIR=/opt/corridor/uploads
```

#### Step 3: Deploy with Docker Compose

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f corridor-app

# Initialize database
docker-compose exec corridor-api corridor-api db upgrade
```

#### Step 4: Configure Reverse Proxy

Create Nginx configuration for Docker deployment:

```nginx
server {
    listen 80;
    server_name corridor.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /jupyter/ {
        proxy_pass http://127.0.0.1:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Best Practices

- Deploy behind a **firewall** with restricted access
- Use **SSL/TLS certificates** for HTTPS access
- Configure **network segmentation** between components
- Enable **audit logging** for all services
- Use **strong passwords** for database and Redis
- Implement **backup strategies** for database and file storage
- Configure **monitoring and alerting** for all services
- Use **process isolation** (containers or separate VMs)
- Enable **automatic security updates**
- Implement **access controls** and user management

## Monitoring and Operations

### Health Checks

```bash
# Check application health
curl -f http://localhost:5002/health

# Check API health
curl -f http://localhost:5003/health

# Check service status (VM)
sudo systemctl status corridor-app corridor-api

# Check container status (Docker)
docker-compose ps
```

### Log Management

```bash
# View application logs (VM)
sudo journalctl -u corridor-app -f

# View container logs (Docker)
docker-compose logs -f corridor-app

# View all service logs
sudo journalctl -u corridor-* -f
```

### Backup Procedures

```bash
# Database backup
pg_dump -h database-server -U corridor corridor > corridor_backup_$(date +%Y%m%d).sql

# File storage backup
tar -czf corridor_data_backup_$(date +%Y%m%d).tar.gz /shared/corridor/

# Configuration backup
tar -czf corridor_config_backup_$(date +%Y%m%d).tar.gz /opt/corridor/instances/default/config/
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify database server is running
   - Check connection string in configuration
   - Ensure firewall allows database connections

2. **Redis Connection Issues**
   - Verify Redis server is running
   - Check Redis URL configuration
   - Ensure Redis is accessible from all services

3. **File Storage Issues**
   - Verify shared storage is mounted
   - Check file permissions
   - Ensure all services can access the storage

4. **Service Startup Issues**
   - Check systemd service status
   - Review service logs for errors
   - Verify configuration files are correct

### Performance Optimization

- **Database Tuning**: Optimize PostgreSQL configuration
- **Redis Tuning**: Configure Redis memory settings
- **Storage Optimization**: Use SSD storage for better I/O
- **Network Optimization**: Ensure low latency between components
- **Resource Monitoring**: Monitor CPU, memory, and disk usage
