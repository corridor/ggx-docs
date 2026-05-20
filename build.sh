#!/bin/bash

set -e
set -x

# Build the documentation site with Astro Starlight.
# Output goes to corridor_docs/site with base '/' (required for the offline Flask package).
npm ci
npm run build

# Create the Python wheel (bundles corridor_docs/site via package-data)
python -m build --wheel

[[ ! -d artifacts ]] && mkdir artifacts

# Copy artifacts
mv dist/* artifacts/
