# Self-Hosted GGX
Source: https://docs.genguardx.ai/technology/self-hosting/
Markdown: https://docs.genguardx.ai/technology/self-hosting/index.md
Description: Install, configure, scale, back up, harden, and operate self-hosted GGX instances across Kubernetes, Terraform, cloud, Docker, and manual deployment options.

**Note: Agent Hosting**

For guides on how the analytics and agents written in GGX can be deployed to Production - refer to the [Direct to Production](https://docs.genguardx.ai/deploy-and-monitor/direct-to-production/) guide.

Guides that cover the installation, configuration, and scaling of Self-Hosted GGX instances for analytical use.

- [Minimum Requirements](https://docs.genguardx.ai/technology/self-hosting/installation/minimum-requirements/)
- Installing on your own infrastructure

    - [Kubernetes](https://docs.genguardx.ai/technology/self-hosting/installation/kubernetes/)
    - [Terraform](https://docs.genguardx.ai/technology/self-hosting/installation/terraform/)
    - [Amazon Web Services (AWS)](https://docs.genguardx.ai/technology/self-hosting/installation/aws/)
    - [Microsoft Azure](https://docs.genguardx.ai/technology/self-hosting/installation/azure/)
    - [Google Cloud Platform (GCP)](https://docs.genguardx.ai/technology/self-hosting/installation/gcp/)
    - [Docker-based](https://docs.genguardx.ai/technology/self-hosting/installation/docker-based/)
    - [Manual](https://docs.genguardx.ai/technology/self-hosting/installation/manual/)

- Configurations: How to configure your self-hosted instance of GGX

    - [SSO Integration - Microsoft AD, Okta, Google Workspace, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/saml/)
    - [RDBMS - Oracle, MS SQL Server, Postgres, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/database/)
    - [Web Servers - Nginx, Apache, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/web-servers/)
    - [Integrating packages - Wheelhouse, Artifactory, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/packages/)
    - [Automated Approval Steps - Jenkins, ServiceNow, JIRA, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/approvals/)
    - [Data Lakes - HDFS, Hive, Snowflake, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/datalake/)
    - [Notifications - Email, Slack, Teams, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/notifications/)
    - [Process Management - Systemd, Supervisor, etc.](https://docs.genguardx.ai/technology/self-hosting/configurations/process-management/)

- Scaling to 100s and 1000s of users

    - [Concurrency - Increasing number of parallel runs](https://docs.genguardx.ai/technology/self-hosting/scaling/concurrency/)
    - [Scaling to number of users](https://docs.genguardx.ai/technology/self-hosting/scaling/scalability/)
    - [Backup Management](https://docs.genguardx.ai/technology/self-hosting/scaling/backups/)

- [Hardening your GGX instance](https://docs.genguardx.ai/technology/self-hosting/hardening/)

## Architectural Overview

The GGX analytical layer lets analysts test and validate their logic and get the required approvals and compliance checks. The production layer is NOT described here because GGX is isolated from the production side.

GGX is divided into various components to keep it modular and enable easy scaling for cloud-based deployments and also to manage high loads without much change. Each of the components can be installed on separate machines or any subset can be installed in the same machine.

The components are divided into:

- **Web Application Server**: The web application server for the analytical UI of the platform
- **API Server**: The API for business logic
- **API - Celery worker**: The worker for asynchronous API tasks
- **Spark - Celery worker**: The worker for asynchronous spark tasks
- **Jupyter Notebook**: The Jupyter Notebook server for free-form analytical use
- **File Management**: The file management server to manage files
- **Metadata Database (SQL RDBMS)**: The database with all metadata provided in the Web Application
- **Authentication Provider**: The identity and auth provider for access and permissions
- **Proxy / Load Balancers**: Load Balancers / Proxies to simplify the install

Here is a typical network diagram of how the installation would look like:
*Figure: Network Diagram*
