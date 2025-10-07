---
title: Minimum Requirements
---

This section describes the minimum requirements that are needed for a Corridor Installation.

Broadly, the components involved are:

- Web Application & Worker
- Spark Worker
- Jupyter Notebook
- File Management
- Metadata Database (SQL RDBMS)
- Redis - Messaging Queue

For very simple installations, all of these could be installed on the same machine, we recommend
keeping them separate to simplify scalability needs.

## Web Application

A flask application which serves the User Interface and Web APIs which are accessible to users via the browser.
It also includes a worker process for long running tasks in the API.
This component has 2 processes: `corridor-app` and `corridor-worker`

### Requirements

- RAM: 4 GB
- Processor: 4 CPU
- Installation storage space: 20 GB
- Python 3.11+

Optional:

- Web Server - Example: Nginx
- Process Management - Example: Supervisor or Systemd

## Spark Worker

Worker to handle any jobs triggered by users which are asynchronously.
It is recommended to have at least 2 workers and increase concurrency as required.

!!! note

    This needs to be installed on a machine that is configured as a Spark Gateway (i.e. A
    master node or an edge node of the cluster). This is not the data nodes of the cluster itself.
    The worker process should be able to import the `pyspark` module.

### Requirements

- RAM: 16 GB
- Processor: 8 CPU
- HDFS storage space: 500 GB (depends on the data being processed, HDFS space to handle shuffles need to be considered too)
- Python 3.11+
- Java 8+
- Spark 3.3+

Optional:

- Process Management - Example: Supervisor or Systemd

## Jupyter Notebook

A notebook for free-form analytical usage. We provide Jupyter Notebooks out-of-the-box but can integrate with existing notebook solutions too.

!!! note

    This needs to be installed on a machine that is configured as a Spark Gateway (i.e. A
    master node or an edge node of the cluster). This is not the data nodes of the cluster itself.
    The jupyter notebook kernel should be able to import the `pyspark` module.

### Requirements

- RAM: 4 GB for base services and more as per usage by users
- Processor: 4 CPU and more as per usage by users
- Installation storage space: 10 GB
- Python 3.11+
- Spark 3.3+

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

## Redis - Messaging Queue

A low-latency task queue to send and receive information about the asynchronous tasks.

### Requirements

- RAM: 1 GB
- Processor: 1 CPU
- DB Snapshots storage space: 10 GB
- Redis 4+
