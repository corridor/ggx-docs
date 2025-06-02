# Corridor Documentation

## Pre-requisites

- Python 3.10+
- Weasyprint: <https://weasyprint.readthedocs.io/en/stable/install.html>
    - In Mac: `brew install cairo pango gdk-pixbuf libffi`
    - In Ubuntu: `sudo apt-get install build-essential libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info`

## Setup Summary

To run a mkdocs server, run:

    # Install python deps
    uv venv venv --python 3.11 --seed
    uv pip install -r requirements.txt --python venv

    # Install JS deps -- for prettier formatting
    npm install -g pnpm@9
    pnpm i

After installation, you can serve mkdocs directly with:

    # Serve mkdocs directly
    venv/bin/mkdocs serve

and then access the docs at <http://localhost:8000>

Or you can also run corridor-docs directly:

    # Run corridor-docs locally
    venv/bin/corridor-docs run

## Guidelines on Writing

- Avoid using "the platform" and instead use "Corridor" so readers are clear on what is being said
- Run grammarly on the content to fix any grammar issues and typos
    - Grammarly changes whitespaces to a different ascii space. So, need to do a find replace to bring back spaces correctly, otherwise markdown renderers don't work
    - Grammarly messes up the formatting for admonitions like `!!!note`
