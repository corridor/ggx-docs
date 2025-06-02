# Multiple Corridor Workers

Corridor provides an option to run multiple workers on the same server, without the workers interfering with
each other. The user needs to provide a name for each worker and worker-specific configuration in
api_config.py, where each configuration is tied to the worker's name.

## Custom `corridor-worker run` command with a worker name

The worker name can be provided with the option `--worker-name` or `-n`

- `INSTALL_DIR/venv-api/bin/corridor-worker run --worker-name CUSTOM_`

!!! note

    The worker's name needs to have all **capital letters**. Underscores (`_`) can be part of the worker's name.

## Custom worker configurations

Any worker-specific configuration is required to be added to the file:

- `INSTALL_DIR/instances/INSTANCE_NAME/config/api_config.py`

To avoid synchronization issues with other workers running on the same server. The worker configurations have
to be prefixed with the worker name provided in the `corridor-worker run` command above.

### Configurations

Taking the above `corridor-worker run` command as an example, where the worker name is `CUSTOM_`,
the configurations would be:

- `CUSTOM_WORKER_QUEUES`
- `CUSTOM_WORKER_PIDFILE`
- `CUSTOM_WORKER_LOGFILE`
- `CUSTOM_WORKER_PROCESSES`
- `CUSTOM_CELERY_WORKER_STATE_DB`
- `CUSTOM_CELERY_WORKER_HIJACK_ROOT_LOGGER`
- `CUSTOM_CELERY_WORKER_REDIRECT_STDOUTS`
