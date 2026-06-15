---
title: "Self-Hosted Corridor"
---

:::note[Pipeline Hosting]
For guides on how the analytics and pipelines written in Corridor can be deployed to Production - refer to the [Direct to Production](../../deploy-and-monitor/direct-to-production/) guide.
:::

Guides that cover the installation, configuration, and scaling of Self-Hosted Corridor instances for analytical use.

- [Minimum Requirements](installation/minimum-requirements/)
- Installing on your own infrastructure

    - [Kubernetes](installation/kubernetes/)
    - [Terraform](installation/terraform/)
    - [Amazon Web Services (AWS)](installation/aws/)
    - [Microsoft Azure](installation/azure/)
    - [Google Cloud Platform (GCP)](installation/gcp/)
    - [Docker-based](installation/docker-based/)
    - [Manual](installation/manual/)

- Configurations: How to configure your self-hosted instance of Corridor

    - [SSO Integration - Microsoft AD, Okta, Google Workspace, etc.](configurations/saml/)
    - [RDBMS - Oracle, MS SQL Server, Postgres, etc.](configurations/database/)
    - [Web Servers - Nginx, Apache, etc.](configurations/web-servers/)
    - [Integrating packages - Wheelhouse, Artifactory, etc.](configurations/packages/)
    - [Automated Approval Steps - Jenkins, ServiceNow, JIRA, etc.](configurations/approvals/)
    - [Data Lakes - HDFS, Hive, Snowflake, etc.](configurations/datalake/)
    - [Notifications - Email, Slack, Teams, etc.](configurations/notifications/)
    - [Process Management - Systemd, Supervisor, etc.](configurations/process-management/)

- Scaling to 100s and 1000s of users

    - [Concurrency - Increasing number of parallel runs](scaling/concurrency/)
    - [Scaling to number of users](scaling/scalability/)
    - [Backup Management](scaling/backups/)

- [Hardening your Corridor instance](hardening/)

## Architectural Overview

The Analytical layer of Corridor for analysts to test and validate their logic and get the required approvals and compliance checks. The production layer is NOT described here as Corridor is isolated from the Production side.

Corridor is divided into various components to keep it modular and enable easy scaling for cloud-based deployments and also to manage high loads without much change. Each of the components can be installed on separate machines or any subset can be installed in the same machine.

The components are divided into:

- **Web Application Server**: The web application server for the analytical UI of the platform
- **API Server**: The API for business logic
- **API - Celery worker**: The worker for asynchronous API tasks
- **Spark - Celery worker**: The worker for asynchronous spark tasks
- **Jupyter Notebook**: The Jupyter Notebook server for free-form analytical use
- **File Management**: The file management server to manage files
- **Metadata Database (SQL RDBMS)**: The database with all metadata provided in the Web Application
- **Messaging Queue (Redis)**: The messaging queue to orchestrate worker tasks
- **Authentication Provider**: The identity and auth provider for access and permissions
- **Proxy / Load Balancers**: Load Balancers / Proxies to simplify the install

Here is a typical network diagram of how the installation would look like:
![Network Diagram](./ggx-network-diagram.excalidraw.svg)
