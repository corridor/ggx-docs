# Process Management

For ease of maintenance and monitoring, it is recommended to use a process management tool to ensure
the component daemons are running correctly. Using a process manager can simplify restarts, reboots,
status-checks, logging, and configurations.

The process management tools that are frequently used are Systemd, init-script, etc. In general, it
is recommended to use the tool that the OS provides to handle these tasks.

To simplify the installation, Supervisor can also be used, which provides application-level process
management that is independent of the host setup.

The tools available for process management require `sudo` access which might not be an option in some situations.
Corridor has its own process manager for each of the components, which uses daemonisation to handle long-running,
background processes.

## Daemon Mode

No additional configurations are required when running Corridor processes using Corridor-Daemons.
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

To use corridor with Supervisor, some useful configurations are:

- `command`: The command to execute. Note, if 2 commands need to be executed, use `bash -c "command1; command2"`
- `stdout_logfile`: Log file location for the stdout logs (`%(program_name)s` and `%(process_num)01d` can be used as variables)
- `stderr_logfile` or `redirect_stderr`: Log file location for the stderr logs, or redirect all the stderr logs to the stdout stream and hence have a common file for both
- `user`: The user to run the process as
- `environment`: The environment variables to be set before the process is run
- `numprocs`: The number of processes to run

Here are some example configuration files for the Corridor components:

**Web Application server:**

```ini
[program:corridor-app]
command=INSTALL_DIR/venv-app/bin/corridor-app run
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=root
```

**API server:**

```ini
[program:corridor-api]
command=
  bash -c "INSTALL_DIR/venv-api/bin/corridor-api db upgrade && INSTALL_DIR/venv-api/bin/corridor-api run"
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=root
```

**API - Celery worker:**

```ini
[program:corridor-worker-api]
command=INSTALL_DIR/venv-api/bin/corridor-worker run --queue api
environment=
  C_FORCE_ROOT=1
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=root
```

**Spark - Celery worker:**

```ini
[program:corridor-worker-spark]
command=INSTALL_DIR/venv-api/bin/corridor-worker run --queue spark --queue quick_spark
environment=
  C_FORCE_ROOT=1
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=root
```

**Jupyter Notebook:**

```ini
[program:corridor-jupyter]
command=INSTALL_DIR/venv-jupyter/bin/corridor-jupyter run
stdout_logfile=/var/log/corridor/%(program_name)s.log
redirect_stderr=true
user=root
```

## Systemd

Many Linux OS like RHEL have systemd pre-installed. To use systemd, the following steps need to be followed:

- Add service file to systemd services folder. For example: `/etc/systemd/system/corridor.service`
- To start service: `sudo systemctl start corridor`  
  And to run the service on startup: `sudo systemctl enable corridor`

Here are some example configuration files for the Corridor components:

**Web Application server:**

```ini
[Unit]
Description=Corridor Web Application
After=syslog.target network.target

[Service]
User=root
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-app/bin/corridor-app run \
  >> /var/log/corridor/corridor-app.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**API server:**

```ini
[Unit]
Description=Corridor API
After=syslog.target network.target

[Service]
User=root
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-api run \
  >> /var/log/corridor/corridor-api.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**API - Celery worker:**

```ini
[Unit]
Description=Corridor Worker API
After=syslog.target network.target

[Service]
User=root
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-worker run --queue api \
  >> /var/log/corridor/corridor-worker-api.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**Spark - Celery worker:**

```ini
[Unit]
Description=Corridor Worker Spark
After=syslog.target network.target

[Service]
User=root
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-worker run --queue spark --queue quick_spark \
  >> /var/log/corridor/corridor-worker-spark.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```

**Jupyter Notebook:**

```ini
[Unit]
Description=Corridor Jupyter
After=syslog.target network.target

[Service]
User=root
ExecStart=/bin/bash -c 'INSTALL_DIR/venv-api/bin/corridor-jupyter run \
  >> /var/log/corridor/corridor-jupyter.log 2>&1'
Restart=always

[Install]
WantedBy=multi-user.target
```
