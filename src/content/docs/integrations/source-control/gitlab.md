---
title: "GitLab"
description: "Connect gitlab.com or a self-managed GitLab so projects can clone, sync, and push Code Repos, and create GitLab issues from GGX."
---

[GitLab](https://about.gitlab.com/) hosts code repositories. GGX uses one GitLab connection for the organization. It serves both GitLab issues and Code Repos, on gitlab.com or on your own GitLab server.

## What it does in GGX

- Clone GitLab projects into a project's **Code Repos**, sync them, and push changes. You see the projects you are a member of, including those in groups and subgroups.
- Sync and push use your own GitLab account.
- The same connection serves GitLab issues, so people sign in once.

## How an administrator sets it up

1. Open **Org Settings → Integrations** and select **GitLab**. It is listed under Source Control and under Issue Trackers.
2. In GitLab, open your user settings, then **Applications**, and add a new application named GenGuardX. Enter the redirect URI the dialog shows, and keep **Confidential** checked.
3. Select the scopes the dialog lists. `api` lets GGX create issues. `read_repository` and `write_repository` let it clone, sync, and push Code Repos.
4. Paste the **Application ID** and **Secret** into GGX. For a self-managed GitLab, also enter **GitLab URL**: the HTTPS root of the server, with no path. Leave it empty for gitlab.com. It applies to the whole organization.
5. Save.

If the application was registered earlier for GitLab issues only, edit it in GitLab to add the two repository scopes. People then connect again.

Turn on **Let people connect with a personal API token** if you want to allow personal access tokens as well as sign-in.

## How to connect your account

1. Open **Code Repos** in a project, choose **More providers**, and select **GitLab**.
2. Select **Connect GitLab**, then sign in. If your administrator allows it, you can connect with a personal access token instead. A token needs the scopes `read_repository` and `write_repository`, and `read_api` as well for issues.
3. Pick the project to clone from **Projects you are a member of**, and give it a **Name in GGX**.

If the list is empty or cloning fails, check that your connection has the two repository scopes, then reconnect. Use **Manage connection** to review or disconnect your account.

## Notes

- Clone brings in the branches and commit history.
- Disconnecting removes both your issue and repository access.
