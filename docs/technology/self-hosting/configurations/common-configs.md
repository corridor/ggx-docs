---
title: Common Configs
---

After the installation, there are some configurations that need to be configured for each of the
components. This section describes all the available configurations needed for each component to
work correctly. Using these configurations the setup can be tweaked as needed.

The configurations for each component needs to be present in the corresponding config file:

- `api_config.py`: For the API Server and Celery Tasks
- `app_config.py`: For the Web Application Server
- `jupyterhub_config.py`: For the Jupyter Notebook (Jupyterhub)
- `jupyter_notebook_config.py`: For the Jupyter Notebook (Notebook server)

## Configuration using Environment Variables

It is possible to configure the platform using environment variables instead of (or in combination with)
config files mentioned above. This might be more convenient in a cloud based deployment setting or while using
a centralized secret management system (like Hashicorp Vault).

When working with secret management systems, configurations could be loaded as environment variables during deployment of the platform.

When configuring API/APP component via environment variables, prepend the configuration key with `CORRIDOR_`.
Below are some examples for some standard data types,

| Setting in `api_config.py`                        | Environment Variable Equivalent                                   |
| ------------------------------------------------- | ----------------------------------------------------------------- |
| `LICENSE_KEY = xxxxxxx`                           | `export CORRIDOR_LICENSE_KEY=xxxxxxx`                             |
| `WORKER_PROCESSES = 1`                            | `export CORRIDOR_WORKER_PROCESSES=1`                              |
| `REQUIRE_SIMULATION = False`                      | `export CORRIDOR_REQUIRE_SIMULATION=false`                        |
| `WORKER_QUEUES = ['api', 'spark', 'quick_spark']` | `export CORRIDOR_WORKER_QUEUES="['api', 'spark', 'quick_spark']"` |

## API

The API Configurations help in controlling how the API Server and Celery workers behave.

Some of the commonly used configurations are:

- `LICENSE_KEY`: The corridor license-key to use to enable the application
- `API_KEYS`: The API keys to accept requests from
- `SQLALCHEMY_DATABASE_URI`: The Database URI to connect to for the Metadata Database
- `FS_URI`: The FileSystem URI to connect to for File Management
- `CELERY_BROKER_URL`: The URL of the Celery Broker (The Redis server for task queue management)
- `CELERY_RESULT_BACKEND`: The URL of the Celery Backend (The Redis server for task queue management)

## Web Application

These configurations help in controlling how the Web Application Server behaves.

Some of the commonly used configurations are:

- `SECRET_KEY`: Ensure a unique secret key for your setup is used
- `REST_API_SERVER_URL`: The URL of the API Server for business login and metadata
- `REST_API_KEY`: The API Key to use when connecting to the API Server
- `NOTEBOOK_CONFIGS__link`: URL to a notebook solution

## Jupyter

The Jupyter configurations are divided into 2 sections: jupyterhub and jupyter-notebook configurations.

## JupyterHub Configurations

The configurations used by the Corridor Platform are the same as the standard [Jupyter Hub configurations](https://jupyter-notebook.readthedocs.io/en/stable/configuring/config_overview.html).

Some of the commonly used configurations are:

- `c.JupyterHub.bind_url`: The URL to host JupyterHub on
- `c.Authenticator.auth_api_url`: The Corridor Web Application Server (When using the Corridor Authentication)
- `c.Spawner.env_keep`: And environment variables to be kept when spawning the user jupyter-notebooks
- `c.Authenticator.auth_api_url`: The API for the Authentication. The URL of the Web Application Server.

There are also additional env variables needed by the `corridor` Python Package:

- `os.environ['CORRIDOR_API_URL']`: The Corridor API Server URL
- `os.environ['CORRIDOR_API_KEY']`: The Corridor API Key to use (if set)
