#!/bin/bash

set -e
set -x

: "${ENABLE_PDF_EXPORT:=1}"
export ENABLE_PDF_EXPORT

echo "ENABLE_PDF_EXPORT is set to $ENABLE_PDF_EXPORT"


# Build the docs using mkdocs
venv/bin/mkdocs build --site-dir corridor_docs/site

# Create package
venv/bin/python -m build --wheel

[[ ! -d artifacts ]] && mkdir artifacts

# Copy artifacts
mv dist/* artifacts/
