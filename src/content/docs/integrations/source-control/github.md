---
title: "GitHub"
description: "Connect GitHub accounts to GGX to clone, sync, and push the code repositories of a project, and to create GitHub issues from GGX issues."
---

[GitHub](https://github.com/) hosts code repositories. GGX uses a GitHub connection so that a project's Code Repos can be cloned from, synced with, and pushed to GitHub.

## What it does in GGX

- Clone repositories into a project's **Code Repos**, sync them, and push changes.
- The repositories you can choose are those your GitHub account can access and where the GenGuardX GitHub App is installed.
- The same connection serves [GitHub Issues](../../issue-trackers/github-issues/), so no second sign-in is needed.

## How to connect

1. Each person opens **My Account → Integrations** and connects their GitHub account through the GenGuardX GitHub App.
2. Use **Manage GitHub access** to install the app on more accounts or organizations and choose which repositories it can reach.
3. Administrators can see connected accounts and disconnect one in **Org Settings → Integrations → GitHub**. The Code Repos clone dialog is where repositories are picked.

## Notes

- Disconnecting removes the saved GGX credentials; it keeps your GitHub installations and local Code Repos.
- GitHub validates access when you perform a repository operation.
- For a GitHub server your organization hosts, see [GitHub Enterprise Server](../github-enterprise-server/).
