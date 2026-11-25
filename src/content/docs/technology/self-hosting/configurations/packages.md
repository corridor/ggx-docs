---
title: "Additional Libraries"
description: "Install and manage additional Python libraries for self-hosted GGX components, notebooks, workers, and analytical workloads."
---

GGX provides an option to allow the users to be able to use additional libraries which are not available
out of the box.

## Configuration

Python code runs in the kernels of the [kernel worker](../process-management/#kernel-runtime), in an environment that GGX builds for each project from its Python packages, so a library does not need to be installed on the servers. To let the user validate the definition and run successful jobs on the platform:

1. Add the library in **Settings > Python Packages** (for the organization or for a project). GGX builds the environment with it the first time that it is needed.
2. Add the library to the Allowed Python Imports in the `Platform Settings` tab in the platform UI


## Frequently asked questions

### Do I need to install libraries on the GGX servers?

No. GGX builds a Python environment for each project from its configured packages, and code runs in the kernels of the kernel worker inside that environment, so nothing is installed on the servers themselves.

### Why is my library import rejected?

The library must be added in two places: **Settings > Python Packages** so it is installed, and the Allowed Python Imports in the `Platform Settings` tab so definitions that import it validate and run.
