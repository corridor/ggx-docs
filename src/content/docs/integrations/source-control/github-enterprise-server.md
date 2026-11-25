---
title: "GitHub Enterprise Server"
description: "Connect a GitHub Enterprise Server your organization runs so projects can clone, sync, and push Code Repos from it."
---

GitHub Enterprise Server is the GitHub product you host yourself. GGX works with it the same way it works with [GitHub](../github/), against your own server address.

## What it does in GGX

- Clone repositories from your server into a project's **Code Repos**, sync them, and push changes.
- Each person connects with a GitHub App you register on your server, or with a personal access token.

## How an administrator sets it up

1. Open **Org Settings → Integrations → Source Control** and select **GitHub Enterprise Server**.
2. Follow **Register the GitHub App on your server**. The dialog gives the two URLs to enter in GitHub (Callback URL and Setup URL) and the permissions to set: **Contents** with read and write, and **Metadata** with read-only. GGX uses no webhooks, and the dialog tells you which two options to turn off when you register the app.
3. Enter the values from your server:
   - **Base URL**: the root of your server, such as `https://github.example.com`. It must be HTTPS with no path. This is the only required value.
   - **App slug**: the last part of the app's URL on your server.
   - **Client ID** and **Client secret**: from the app. The secret is write-only: GGX encrypts it and never shows it again. Leave it empty to keep the saved one.
4. Save.

Without the app, people cannot use **Connect with the GitHub App**, but they can still connect with a personal access token.

The dialog also lists connected users, and you can disconnect one. **Remove** deletes the server configuration.

:::caution
Saving a different base URL disconnects every user, because a token is valid only on its own server.
:::

## How to connect your account

1. Open **Code Repos** in a project, choose **More providers**, and select **GitHub Enterprise Server**.
2. Select **Connect with the GitHub App**, sign in on your server, then install the app or choose its repositories. Or select **Use a personal access token**.
3. For a token, a classic token needs the `repo` scope. A fine-grained token needs read and write access to **Contents** on the repositories it should reach. GGX stores the token encrypted and never shows it again.
4. Pick the repository to clone and give it a **Name in GGX**.

If a repository is missing from the list, select **Manage GitHub Enterprise Server access** to install the app on the account that owns it. A personal access token reaches only the repositories of its owner.

## Notes

- Disconnecting removes your saved credentials. Local Code Repos stay available.
- Clone brings in the branches and commit history.
