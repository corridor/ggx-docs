---
title: "JupyterHub"
description: "Connect your JupyterHub to GGX so users can open managed Jupyter notebooks from the platform."
---

[JupyterHub](https://jupyter.org/hub) serves managed Jupyter notebook environments to many users. GGX can open your JupyterHub as an IDE for working with notebooks.

## What it does in GGX

- Offer your JupyterHub as a notebook environment alongside the platform.
- Forward selected user details to the hub when it opens, for hubs that need them to sign users in.

## How to connect

1. In GGX, open **Org Settings → Integrations → IDE providers** and select **JupyterHub**.
2. Enter the URL of your JupyterHub.
3. Optionally choose the query parameters to send when the IDE opens (user ID, user token, user name, or user email).
4. Save.

## Notes

- Of the IDE providers, JupyterHub is the one you configure yourself.
