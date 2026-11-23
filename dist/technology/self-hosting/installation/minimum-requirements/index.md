# Minimum Requirements
Source: https://docs.genguardx.ai/technology/self-hosting/installation/minimum-requirements/
Markdown: https://docs.genguardx.ai/technology/self-hosting/installation/minimum-requirements/index.md
Description: Review the minimum CPU, memory, storage, database, kernel worker, Python, web server, and process management requirements for self-hosted GGX components.

This section describes the minimum requirements that are needed for a GGX installation.

Broadly, the components involved are:

- Web Application
- Kernel Worker
- Jupyter Notebook
- File Management
- Metadata Database (SQL RDBMS)

For very simple installations, all of these could be installed on the same machine, we recommend
keeping them separate to simplify scalability needs.

## Web Application

A flask application which serves the User Interface and Web APIs which are accessible to users via the browser.
This component has the process `corridor-app`; the kernel worker (`corridor-worker`) is described below.

### Requirements

- RAM: 4 GB
- Processor: 4 CPU
- Installation storage space: 20 GB
- Python 3.11+

Optional:

- Web Server - Example: Nginx
- Process Management - Example: Supervisor or Systemd

## Kernel Worker

The worker (`corridor-worker run`) that owns the Jupyter kernels, where all Python code runs: chats, Debug Code, deployments, figures, data previews, and the background jobs. By default, up to 4 kernels run at the same time, 2 of them for jobs. See [Kernel Runtime](https://docs.genguardx.ai/technology/self-hosting/configurations/process-management/#kernel-runtime).

**Note**

The kernel worker and the API server use the same files (the kernel environments, and the files that jobs read and write): run them on the same machine, or give both the same shared storage.

### Requirements

- RAM: 16 GB (each kernel needs the memory of the data and code that it runs)
- Processor: 8 CPU
- Storage space: for the kernel environments (which depend on the Python packages of the projects) and the data being processed
- Python 3.11+
- Access to a Python package index, to build the environments of the projects

Optional:

- Process Management - Example: Supervisor or Systemd

## Jupyter Notebook

A notebook for free-form analytical usage. We provide Jupyter Notebooks out-of-the-box but can integrate with existing notebook solutions too.

### Requirements

- RAM: 4 GB for base services and more as per usage by users
- Processor: 4 CPU and more as per usage by users
- Installation storage space: 10 GB
- Python 3.11+

Optional:

- Process Management - Example: Supervisor or Systemd

## File Management

A file system management to store and retrieve files. A NAS storage that can be mounted on all servers and be accessible by all services is ideal.

### Requirements

- File storage space: 50 GB

## Metadata Database

This serves as an internal RDBMS to store the state of the application and various user information.

### Requirements

- RAM: 2 GB
- Processor: 2 CPU
- Database storage space: 5 GB

- SQL Databases supported:

    - Oracle 19+
    - MSSQL 2016+
    - Postgres 11.7+
