---
title: "IDE providers"
description: "Open JupyterHub, Google Colab, Visual Studio Code or GitHub Codespaces from GGX, and see which of them you configure yourself."
---

IDE providers give users a development environment to open from GGX. They are listed in **Org Settings → Integrations** under **IDE/Notebook Integrations**.

| Integration | What it does | Who sets it up |
| --- | --- | --- |
| [JupyterHub](jupyterhub/) | Managed Jupyter notebooks on your own JupyterHub. | An organization administrator, in **Org Settings → Integrations**. |
| [Google Colab](google-colab/) | Work with notebooks on Google Colab. | The GGX Team. |
| [Visual Studio Code](visual-studio-code/) | Browser-based VS Code development environment. | The GGX Team. |
| [GitHub Codespaces](github-codespaces/) | Codespaces hosted on GitHub. | The GGX Team. |

## How users open an IDE

Once an IDE is configured for the organization, its name appears under **IDEs** in the profile menu. Selecting it opens the configured URL in a new browser tab. Which user details are added to that URL depends on the query parameters saved with the integration. See [JupyterHub](jupyterhub/) for the list.

## Notes

- Only JupyterHub opens a configuration dialog. For the other three, selecting **Configure** shows the message "Not available - contact the GGX Team to configure this".
