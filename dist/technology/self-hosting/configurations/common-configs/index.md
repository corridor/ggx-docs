# Common Configs
Source: https://docs.genguardx.ai/technology/self-hosting/configurations/common-configs/
Markdown: https://docs.genguardx.ai/technology/self-hosting/configurations/common-configs/index.md
Description: Configure common self-hosted GGX settings for application services, API behavior, storage, authentication, workers, notebooks, and logging.

After the installation, there are some configurations that need to be configured for each of the
components. This section describes all the available configurations needed for each component to
work correctly. Using these configurations the setup can be tweaked as needed.

The configurations for each component needs to be present in the corresponding config file:

- `api_config.py`: For the API Server and the kernel worker
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
| `KERNEL_MAX_PROCESSES = 4`                        | `export CORRIDOR_KERNEL_MAX_PROCESSES=4`                          |
| `REQUIRE_SIMULATION = False`                      | `export CORRIDOR_REQUIRE_SIMULATION=false`                        |
| `KERNEL_ALLOWED_ENVIRONMENT = ['PATH', 'UV_*']`   | `export CORRIDOR_KERNEL_ALLOWED_ENVIRONMENT="['PATH', 'UV_*']"`   |

## API

The API Configurations help in controlling how the API Server and the kernel worker behave.

Some of the commonly used configurations are:

- `LICENSE_KEY`: The GGX license key to use to enable the application
- `API_KEYS`: The API keys to accept requests from
- `SQLALCHEMY_DATABASE_URI`: The Database URI to connect to for the Metadata Database
- `FS_URI`: The FileSystem URI to connect to for File Management
- `OUTPUT_DATA_LOCATION`: Where job results are written as Parquet files, for example `file:///opt/corridor/instances/default/data/results/{}.parquet`. The `{}` is replaced by the name of the result, and a local folder is created if it does not exist
- `KERNEL_WORKER_URL`, `KERNEL_MAX_PROCESSES`, `KERNEL_ENV_DIR`: Where the kernel worker is, how many kernels run, and where their environments are kept. See [Kernel Runtime](https://docs.genguardx.ai/technology/self-hosting/configurations/process-management/#kernel-runtime)

On Azure, GGX can log in to the Metadata Database with a managed identity instead of a password: see [Azure](https://docs.genguardx.ai/technology/self-hosting/installation/azure/#database-login-with-a-managed-identity).

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

The configurations used by the GGX are the same as the standard [Jupyter Hub configurations](https://jupyter-notebook.readthedocs.io/en/stable/configuring/config_overview.html).

Some of the commonly used configurations are:

- `c.JupyterHub.bind_url`: The URL to host JupyterHub on
- `c.Authenticator.auth_api_url`: The GGX Web Application Server (When using the GGX Authentication)
- `c.Spawner.env_keep`: And environment variables to be kept when spawning the user jupyter-notebooks
- `c.Authenticator.auth_api_url`: The API for the Authentication. The URL of the Web Application Server.

There are also additional env variables needed by the GGX Python package:

- `os.environ['CORRIDOR_API_URL']`: The GGX API Server URL
- `os.environ['CORRIDOR_API_KEY']`: The GGX API Key to use (if set)
