---
title: Install On-Premises
---

This guide provides an overview of deploying Corridor on-premises or in your own data center infrastructure.

## Deployment Options

### Option 1: Bare Metal / Virtual Machines

Deploy Corridor directly on physical servers or virtual machines using the installation bundle.

**Best for:**

- Organizations with existing VM infrastructure
- Traditional IT infrastructure patterns
- Direct control over the operating system
- Simpler operational model without containers

[View VM Installation Guide →](./bundle-install.md)

### Option 2: Docker Containers

Deploy Corridor using Docker containers for a containerized deployment.

**Best for:**

- Organizations using Docker/container infrastructure
- Simplified deployment and updates
- Resource isolation
- Modern infrastructure patterns

[View Docker Installation Guide →](./docker.md)

## Common Requirements

Both deployment options require:

- **Metadata Database**: PostgreSQL, Oracle, or SQL Server
- **Message Queue**: Redis for Celery task orchestration
- **File Storage**: Network-attached storage (NAS) or local storage
- **Web Server**: Nginx or Apache (for production)
- **Process Management**: Systemd or Supervisor
- **SSL Certificates**: For HTTPS access

## Choosing the Right Option

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

## Installation Overview

### VM Installation Process

1. Install system dependencies (Python 3.11+, Java 8+ for Spark)
2. Extract Corridor installation bundle
3. Run installation script for each component
4. Configure connections to database, Redis, and storage
5. Setup process management (systemd/supervisor)
6. Configure web server (Nginx/Apache)

### Docker Installation Process

1. Setup Docker Engine and Docker Compose
2. Pull or build Corridor container images
3. Create docker-compose.yml configuration
4. Configure environment variables and volumes
5. Start containers using docker-compose
6. Configure reverse proxy for external access

