---
title: Install using scripts
---

This section describes the method to do a manual installation of Corridor.

There is a command-line interface available with each component that is installed:

- Web Application Server: `corridor-app`
- API Server: `corridor-api`
- API - Celery worker: `corridor-worker`
- Spark - Celery worker: `corridor-worker`
- Jupyter Notebook: `corridor-jupyter`

## Pre Requisites

Before starting, ensure that the [Minimum Requirements and System Dependencies](./minimum-requirements.md) are met.

## Installation

To perform an install, take the installation bundle provided and extract it into a temporary
location and run the `install` script inside it:

```sh
unzip corridor-bundle.zip
sudo ./corridor-bundle/install [app | api | worker-api | worker-spark | jupyter]
```

When installing, install the specific components of the platform that are required. This will set:

- An appropriate virtual-environment inside the provided installation path
- The configuration file for the component in that section

The complete set of arguments for the installation can be checked with `./corridor-bundle/install -h`:

```none
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

## Running the Application

Once the installation of the component is done, it can be run using the provided command-line tool
for that component. Also, each component has 1 or more configuration files that may need changes.

### Web Application Server

- Configuration File: `INSTALL_DIR/instances/INSTANCE_NAME/config/app_config.py`
- Run application server: `INSTALL_DIR/venv-app/bin/corridor-app run`
- The WSGI application: `corridor_app.wsgi:app`

!!! note

    The web server (`corridor-app run`) can be used for production, by setting the `WSGI_SERVER` config
    to gunicorn or auto. **Avoid using Werkzeug for production.**

### API Server

- Configuration File: `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`
- Run application server: `INSTALL_DIR/venv-api/bin/corridor-api run`
- The WSGI application: `corridor_api.wsgi:app`

To initialize the database, `corridor-api db upgrade` needs to be run.

!!! note

    The web server (`corridor-api run`) can be used for production, by setting the `WSGI_SERVER` config
    to gunicorn or auto. **Avoid using Werkzeug for production.**

### API - Celery worker

- Configuration File: `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`
- Run celery worker: `INSTALL_DIR/venv-api/bin/corridor-worker run --queue api`

!!! note

    If the process is running as the root user, the env variable `C_FORCE_ROOT=1` needs to be set.

### Spark - Celery worker

- Configuration File: `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`
- Run celery worker: `INSTALL_DIR/venv-api/bin/corridor-worker run --queue spark --queue quick_spark`

!!! note

    If the process is running as the root user, the env variable `C_FORCE_ROOT=1` needs to be set.

### Jupyter Notebook

- Configuration File:

    - Jupyter Hub: `INSTALL_DIR/instances/INSTANCE_NAME/config/jupyterhub_config.py`
    - Jupyter Notebook: `INSTALL_DIR/instances/INSTANCE_NAME/config/jupyter_notebook_config.py`

- Run jupyterhub server: `INSTALL_DIR/venv-jupyter/bin/corridor-jupyter run`
