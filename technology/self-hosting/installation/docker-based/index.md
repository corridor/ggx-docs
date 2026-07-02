# Docker-based
Source: https://docs.genguardx.ai/technology/self-hosting/installation/docker-based/
Markdown: https://docs.genguardx.ai/technology/self-hosting/installation/docker-based/index.md
Use a Docker-based deployment when you already operate Docker hosts or Docker Compose and want a containerized GGX installation without adopting Kubernetes.

GGX provides production-ready Dockerfile templates with the installation bundle. Because Docker networking, storage, reverse proxies, and secret management vary significantly by organization, work with GGX support to align the final compose or runtime configuration with your environment.

## Components

| Component | Implementation options |
|---|---|
| Web application | GGX app container behind a reverse proxy |
| API and workers | GGX worker containers for API and Spark queues |
| Jupyter | Jupyter container or integration with an existing notebook service |
| File management | Host mount, Docker volume, or network-attached persistent storage |
| Metadata database | External PostgreSQL, Oracle, SQL Server, or managed database service |
| SSL certificates | Mounted read-only from host storage or injected during image build |
| Platform configuration | Mounted read-only files, environment variables, or approved secret store |

## Requirements

- Docker Engine 20.10 or later.
- Docker Compose or an equivalent orchestration process if running multiple containers manually.
- Persistent storage for uploads, notebooks, data, state, and backups.
- Metadata database that meets the [minimum requirements](../minimum-requirements/).
- Reverse proxy such as Nginx, Apache, an ingress appliance, or a cloud load balancer.
- TLS certificate for browser-facing traffic.

## Deployment Flow

1. Prepare the host, Docker runtime, persistent storage, database, DNS, and TLS certificate.
2. Build or pull the GGX images provided for your release.
3. Configure shared volumes for data, notebooks, uploads, Jupyter state, and backups.
4. Configure application settings through mounted config files or environment variables.
5. Start the app, worker, Jupyter, and supporting containers.
6. Run database migrations.
7. Configure the reverse proxy so `/` reaches the app service and `/jupyter` reaches the Jupyter service.
8. Verify logs, health checks, persistent storage, and user login.

## Configuration Notes

- Keep the database outside the app container for production deployments.
- Use named volumes or network storage rather than ephemeral container filesystems.
- Store secrets in your platform secret store instead of hard-coding them in compose files.
- Separate app, worker, and Jupyter logs so operations teams can troubleshoot independently.
- Align CPU and memory reservations with the [minimum requirements](../minimum-requirements/).

## When To Choose Another Path

- Use [Kubernetes](../kubernetes/) for managed container orchestration on AKS, GKE, or EKS.
- Use [Terraform](../terraform/) for cloud-managed container services such as ECS Fargate, Azure Container Apps, or Cloud Run.
- Use [Manual](../manual/) for VM or bare-metal installations that do not use containers.