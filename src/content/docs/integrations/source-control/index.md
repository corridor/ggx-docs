---
title: "Source control"
description: "Connect GitHub, GitHub Enterprise Server, GitLab, Bitbucket Cloud or any Git server so projects can clone, sync, and push code repositories."
---

Source control integrations let a project keep its code in Code Repos that are cloned from, synced with, and pushed to your repository host. Administrators turn a host on once for the organization in **Org Settings → Integrations → Source Control**. Each person then connects their own account, and GGX uses that account for every clone, sync, and push.

| Integration | What it does |
| --- | --- |
| [GitHub](github/) | Clone, sync, and push repositories on github.com, and serve GitHub Issues. |
| [GitHub Enterprise Server](github-enterprise-server/) | The same, against a GitHub server your organization runs. |
| [GitLab](gitlab/) | Clone, sync, and push projects on gitlab.com or a self-managed GitLab. The connection also serves GitLab issues. |
| [Bitbucket](bitbucket/) | Clone, sync, and push repositories on Bitbucket Cloud. |
| [Other Git server](git-server/) | Clone, sync, and push over HTTPS or SSH from any Git server, such as Gitea, Gerrit, or an in-house server. |

In a project, open **Code Repos** and use **Clone** for GitHub or **More providers** for the others. A provider that an administrator has not set up shows **Not enabled yet**. See [Code Repos](../../register-and-refine/inventory-management/#code-repos) for what you can do once a repository is in GGX.
