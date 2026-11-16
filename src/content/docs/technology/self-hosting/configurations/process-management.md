---
title: "Process Management"
description: "Run self-hosted GGX services and the kernel worker under systemd or Supervisor, and configure the kernel runtime, its environments, limits, and variables."
---

For ease of maintenance and monitoring, it is recommended to use a process management tool to ensure
the component daemons are running correctly. Using a process manager can simplify restarts, reboots,
status-checks, logging, and configurations.

The process management tools that are frequently used are Systemd, init-script, etc. In general, it
is recommended to use the tool that the OS provides to handle these tasks.

To simplify the installation, Supervisor can also be used, which provides application-level process
management that is independent of the host setup.

The tools available for process management require `sudo` access which might not be an option in some situations.
GGX has its own process manager for each of the components, which uses daemonisation to handle long-running,
background processes.

## Kernel Runtime

All Python that GGX runs for its users executes in Jupyter kernels, outside the API process: chats, Debug Code, deployments, figures, data previews, and the background jobs (simulations and annotation queue ingestions). The kernels belong to the **kernel worker**, a process of its own that is started with `corridor-worker run`.

The kernel worker is a plain Jupyter server. It listens on `KERNEL_WORKER_HOST` and `KERNEL_WORKER_PORT` (by default `127.0.0.1` and `5001`), and the API reaches it with a token that is derived from `SECRET_KEY`, so the API and the worker must use the same `SECRET_KEY`. When the worker is not on the host and port above (for example, a service in a cluster), set `KERNEL_WORKER_URL` in the API configuration, such as `http://corridor-worker-service:5001`.

### Environments

Each project gets a [uv](https://docs.astral.sh/uv/) environment for its Python packages, and a shared uv cache avoids downloading the same package twice. Both are created in `<CONFIG_DIR>/kernels`, in the folders `envs` and `uv-cache`. Set `KERNEL_ENV_DIR` to keep them in another base folder. An environment that was not used for 14 days is removed and is rebuilt when it is needed again.

The API and the worker must see this folder at the same path, so on separate servers or containers it is a shared disk or volume. Keep the environments and the cache on one file system so that uv can link the files instead of copying them.

### Limits

| Setting | Default | Meaning |
| --- | --- | --- |
| `KERNEL_MAX_PROCESSES` | `4` | The number of kernels that can run at the same time, across all API workers |
| `KERNEL_MAX_JOB_PROCESSES` | `2` | Of those, how many can run background jobs (simulations and ingestions) at once. The rest are left for chats and other requests |
| `KERNEL_MAX_TEST_GENERATION_PROCESSES` | `2` | Of those, how many can run the tests that Corra generates for a feedback portal |
| `KERNEL_IDLE_TIMEOUT` | `900` seconds (15 minutes) | How long a kernel that nobody uses stays alive |
| `JOB_TIME_LIMIT` | `7200` seconds (2 hours) | How long a background job can run before it is stopped |

When the limit is reached, a chat turn or a job waits for a kernel, and jobs start in the order that they were queued. A short request, such as a figure or a data preview, gives up after 60 seconds and tells the user that every kernel is busy. See [Concurrency](../../scaling/concurrency/) for sizing.

### Environment variables of the kernels

A kernel only inherits the environment variables that `KERNEL_ALLOWED_ENVIRONMENT` lists: the defaults are `PATH`, `HOME`, the locale and temporary folder variables, proxy and TLS certificate settings, and the `AWS_*`, `GOOGLE_*`, `AZURE_*`, `UV_*` and `PIP_*` families. The secrets that the API receives, such as the database credentials, are not passed to the kernels. The entries are names or patterns such as `UV_*`, and a list that you set replaces the defaults. Restart the kernel worker after changing it. This setting only filters the variables that the worker has: it cannot create one.

:::caution
A kernel runs as the same operating-system user as the API. Code that runs in a kernel can read every file that this user can read.
:::

### Running the processes together

The API servers, the scheduled tasks (cron) and the kernel worker use the same kernel folder and job files: run them on the same machine, or give them shared storage, as the [Kubernetes manifests](../../installation/kubernetes/) do with a shared volume.

## Daemon Mode

No additional configurations are required when running GGX processes using GGX-Daemons.
We can use the below set of commands to start/stop/check_status.
The logfile and pidfile for each process can be saved at custom locations by using the parameters:

- logfile: location of the log file
- pidfile: location of the pid file

The default logfile directory is: `INSTALL_DIR/instances/INSTANCE/logs`

The default pidfile directory is: `INSTALL_DIR/instances/INSTANCE/pids`

To start the processes, we can do:

```sh
INSTALL_DIR/venv-api/corridor-api daemon start
INSTALL_DIR/venv-api/corridor-worker daemon start
INSTALL_DIR/venv-app/corridor-app daemon start
INSTALL_DIR/venv-jupyter/corridor-jupyter daemon start
```

To stop the processes, we can do:

```sh
INSTALL_DIR/venv-api/corridor-api daemon stop
INSTALL_DIR/venv-api/corridor-worker daemon stop
INSTALL_DIR/venv-app/corridor-app daemon stop
INSTALL_DIR/venv-jupyter/corridor-jupyter daemon stop
```

To check the status of the processes, we can do:

```sh
INSTALL_DIR/venv-api/corridor-api daemon status
INSTALL_DIR/venv-api/corridor-worker daemon status
INSTALL_DIR/venv-app/corridor-app daemon status
INSTALL_DIR/venv-jupyter/corridor-jupyter daemon status
```

## Supervisor

To use GGX with Supervisor, some useful configurations are:

- `command`: The command to execute. Note, if 2 commands need to be executed, use `bash -c "command1; command2"`
- `stdout_logfile`: Log file location for the stdout logs (`%(program_name)s` and `%(process_num)01d` can be used as variables)
- `stderr_logfile` or `redirect_stderr`: Log file location for the stderr logs, or redirect all the stderr logs to the stdout stream and hence have a common file for both
- `user`: The user to run the process as
- `environment`: The environment variables to be set before the process is run
- `numprocs`: The number of processes to run

Here are some example configuration files for the GGX components. They run the processes as a dedicated, non-root user named `corridor`; all the GGX processes, including the kernel worker, should run as the same user, and that user needs to be able to write to the installation and the shared folders.

**Web Application server:**

```ini
[program:corridor-app]
command=INSTALL_DIR/venv-app/bin/corridor-app run
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=corridor
```

**API server:**

```ini
[program:corridor-api]
command=
  bash -c "INSTALL_DIR/venv-api/bin/corridor-api db upgrade && INSTALL_DIR/venv-api/bin/corridor-api run"
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=corridor
```

**Kernel worker:**

```ini
[program:corridor-worker]
command=INSTALL_DIR/venv-api/bin/corridor-worker run
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=corridor
```

**Jupyter Notebook:**

```ini
[program:corridor-jupyter]
command=INSTALL_DIR/venv-jupyter/bin/corridor-jupyter run
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=corridor
```

## Systemd

Many Linux OS like RHEL have systemd pre-installed. To use systemd, the following steps need to be followed:

- Add service file to systemd services folder. For example: `/etc/systemd/system/corridor.service`
- To start service: `sudo systemctl start corridor`  
  And to run the service on startup: `sudo systemctl enable corridor`

Here are some example configuration files for the GGX components:

**Web Application server:**

```ini
[Unit]
Description=GGX Web Application
After=syslog.target network.target

[Service]
User=corridor
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-app/bin/corridor-app run \
  >> /var/log/corridor/corridor-app.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**API server:**

```ini
[Unit]
Description=GGX API
After=syslog.target network.target

[Service]
User=corridor
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-api run \
  >> /var/log/corridor/corridor-api.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**Kernel worker:**

```ini
[Unit]
Description=GGX Kernel Worker
After=syslog.target network.target

[Service]
User=corridor
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-worker run \
  >> /var/log/corridor/corridor-worker.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**Jupyter Notebook:**

```ini
[Unit]
Description=GGX Jupyter
After=syslog.target network.target

[Service]
User=corridor
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-jupyter run \
  >> /var/log/corridor/corridor-jupyter.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```
