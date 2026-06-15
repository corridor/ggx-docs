---
title: "Manual"
---

Use a manual installation when you are deploying Corridor directly on VMs, bare metal, or cloud instances and want direct control over the operating system, process manager, web server, database, and storage.

This path applies to on-premises servers and VM-based cloud deployments such as EC2, Azure VMs, and Compute Engine.

## Prerequisites

Before starting, ensure the [minimum requirements](../minimum-requirements/) are met.

You also need:

- Corridor installation bundle.
- Linux host access with privilege to install packages and create services.
- Python 3.11 or later.
- Java 8 or later for Spark worker functionality.
- Redis 4 or later.
- Metadata database: PostgreSQL 11.7 or later, Oracle 19 or later, or SQL Server 2016 or later.
- Persistent file storage.
- Nginx, Apache, or another production reverse proxy.
- TLS certificate for browser-facing traffic.

## Components

The installation bundle provides command-line entry points for each component:

- Web application server: `corridor-app`
- API server: `corridor-api`
- API Celery worker: `corridor-worker`
- Spark Celery worker: `corridor-worker`
- Jupyter Notebook server: `corridor-jupyter`

## Install Components

Extract the bundle and run the installer for each required component:

```sh
unzip corridor-bundle.zip
sudo ./corridor-bundle/install [app | api | worker-api | worker-spark | jupyter]
```

The installer creates:

- A component-specific virtual environment under the installation path.
- Configuration files under the selected instance name.
- Component entry points for running services.

Check installer options with:

```text
usage: install [-h] [-i INSTALL_DIR] [-n NAME] component

positional arguments:
  component             The component to install. Possible values are: api,
                        app, worker-api, worker-spark, jupyter

optional arguments:
  -h, --help            show this help message and exit
  -e EXTRAS [EXTRAS ...], --extras EXTRAS [EXTRAS ...]
                        The extra packages to install
  -i INSTALL_DIR, --install-dir INSTALL_DIR
                        The location to install the corridor package. Default
                        value: /opt/corridor
  --overwrite           Whether to overwrite the configs if already present.
                        Default behavior is to create config files only if
                        they don't already exist.
```

## Configure The API

Update the API configuration, usually at:

```text
INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py
```

Configure the database connection string, Redis connection, file storage, authentication, email, and other platform settings required by your environment.

Run database migrations:

```sh
INSTALL_DIR/venv-api/bin/corridor-api db upgrade
```

## Run Components

### Web Application Server

- Configuration file: `INSTALL_DIR/instances/INSTANCE_NAME/config/app_config.py`
- Run command: `INSTALL_DIR/venv-app/bin/corridor-app run`
- WSGI application: `corridor_app.wsgi:app`

Set `WSGI_SERVER` to `gunicorn` or `auto` for production. Do not use Werkzeug for production.

### API Server

- Configuration file: `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`
- Run command: `INSTALL_DIR/venv-api/bin/corridor-api run`
- WSGI application: `corridor_api.wsgi:app`

Set `WSGI_SERVER` to `gunicorn` or `auto` for production. Do not use Werkzeug for production.

### API Worker

- Configuration file: `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`
- Run command: `INSTALL_DIR/venv-api/bin/corridor-worker run --queue api`

If the process runs as root, set `C_FORCE_ROOT=1`.

### Spark Worker

- Configuration file: `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`
- Run command: `INSTALL_DIR/venv-api/bin/corridor-worker run --queue spark --queue quick_spark`

The Spark worker should run on a machine configured as a Spark gateway or edge node. It should be able to import `pyspark` and reach the target Spark cluster.

### Jupyter Notebook

- Jupyter Hub configuration file: `INSTALL_DIR/instances/INSTANCE_NAME/config/jupyterhub_config.py`
- Jupyter Notebook configuration file: `INSTALL_DIR/instances/INSTANCE_NAME/config/jupyter_notebook_config.py`
- Run command: `INSTALL_DIR/venv-jupyter/bin/corridor-jupyter run`

## Process Management

Use systemd, Supervisor, or your standard process manager. A typical systemd service follows this shape:

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

After creating services:

```sh
sudo systemctl daemon-reload
sudo systemctl enable corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter
sudo systemctl start corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter
```

## Reverse Proxy

Place Nginx, Apache, or an approved load balancer in front of the application services:

- Route browser traffic for the main app to the web application server.
- Route API traffic to the API server if your topology separates app and API.
- Route `/jupyter` to the Jupyter service.
- Terminate TLS at the reverse proxy or load balancer.
- Set secure cookie and secret configuration values before production use.

## Operations

```sh
sudo systemctl status corridor-api
sudo systemctl restart corridor-api
journalctl -u corridor-api -f
```

For cloud VM deployments, use the provider page for required cloud services:

- [AWS](../aws/) for EC2, RDS, EBS or EFS, Route 53, and AWS security controls.
- [Azure](../azure/) for Azure VMs, Azure Database for PostgreSQL, Azure Files, and Azure networking.
- [GCP](../gcp/) for Compute Engine, Cloud SQL, Filestore or persistent disks, and GCP networking.
