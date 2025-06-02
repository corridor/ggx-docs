set -e
set -x

# Build the docs using mkdocs
ENABLE_PDF_EXPORT=1 venv/bin/mkdocs build --site-dir corridor_docs/docs

# Create package
venv/bin/python setup.py bdist_wheel

# Copy artifacts
mv dist artifacts/
