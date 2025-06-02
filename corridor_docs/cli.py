from __future__ import annotations

import sys

import click
from flask.cli import FlaskGroup, run_command, shell_command

from corridor_docs import create_app


# Override the default flask-cli commands with the add_default_commands=False so that we can make it simple
@click.group(cls=FlaskGroup, create_app=create_app, add_default_commands=False, add_version_option=False)
def main() -> None:
    """Corridor Docs commands."""


for opt in run_command.params:
    if opt.name == "port":
        opt.default = 5005


# Add the default `run` and `shell` commands available in flask
main.add_command(run_command)
main.add_command(shell_command)


if __name__ == "__main__":
    sys.exit(main())
