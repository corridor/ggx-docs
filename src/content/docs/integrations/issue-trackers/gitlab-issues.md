---
title: "GitLab Issues"
description: "Create and link GitLab issues from GGX issues on gitlab.com or a self-managed server, with each person signing in to GitLab or using a personal access token."
---

[GitLab](https://about.gitlab.com/) is a DevSecOps platform with a built-in issue tracker. GGX uses it to turn issues found in annotation queues and feedback portals into GitLab issues. The same GitLab connection also serves Code Repos.

## What it does in GGX

- Create a GitLab issue from a GGX issue (Issues Found), in a project you pick.
- Link an existing issue by `group/project#123` or URL.
- Show each linked issue's status and refresh it in the background and on demand.
- Works with gitlab.com and a self-managed GitLab.

## How to connect

1. An administrator adds an application in GitLab (**User settings**, then **Applications**), keeps **Confidential** checked, and saves its application ID and secret in **Org Settings → Integrations → Issue trackers → GitLab**. The dialog shows the redirect URI and scopes to copy into GitLab. For a self-managed GitLab, also enter its **GitLab URL** (the root of the server, without a path); leave it empty for gitlab.com.
2. Each person opens **My Account → Integrations → GitLab** and signs in with GitLab.
3. Optional: an administrator can tick **Let people connect with a personal API token** in the same dialog. People can then paste a personal access token from their GitLab user settings (**Access tokens**) with the `api` scope, and `read_repository` and `write_repository` for Code Repos. This is off by default, because a personal token acts as its owner.

## Notes

- GitLab issues are open or closed, shown in GGX as Open and Resolved. To use the other GGX statuses (Needs triage, Won't fix, Duplicate), give the issue a scoped label such as `status::Needs triage`. A label that disagrees with the issue's state is ignored.
- The `api` scope is needed to create issues; `read_api` only reads.
