---
title: "Bitbucket"
description: "Connect Bitbucket Cloud so projects can clone, sync, and push Code Repos from your workspaces."
---

[Bitbucket Cloud](https://bitbucket.org/) hosts Git repositories in workspaces. GGX connects to it so a project's Code Repos can be cloned from, synced with, and pushed to Bitbucket.

## What it does in GGX

- Clone repositories from the Bitbucket workspaces you belong to into a project's **Code Repos**, sync them, and push changes.
- Each person connects with an OAuth consumer your administrator registers, or with a token.

## How an administrator sets it up

1. Open **Org Settings → Integrations → Source Control** and select **Bitbucket**.
2. Follow **Register the OAuth consumer in Bitbucket**. In the workspace settings of a workspace you administer, open **OAuth consumers** under **Apps and features** and add a consumer. Enter the Callback URL the dialog shows.
3. Under **Permissions**, tick **Account: Read** and **Repositories: Read and Write**, and leave every other permission unticked. Pushing from GGX needs Write.
4. Copy the consumer's key and secret into **Key (client ID)** and **Secret**. The secret is write-only: GGX encrypts it and never shows it again. Leave it empty to keep the saved one.
5. Save. This turns Bitbucket on for every user.

Without a consumer, people cannot use **Connect with Bitbucket**, but they can still connect with a token. **Turn off** switches Bitbucket off for the organization. The dialog also lists connected users, and you can disconnect one.

## How to connect your account

1. Open **Code Repos** in a project, choose **More providers**, and select **Bitbucket**.
2. Select **Connect with Bitbucket**, sign in on Bitbucket, and approve the access.
3. Or select **Use a token**. For an API token, create it in your Atlassian account settings with at least read access to your account, workspaces and repositories, and write access to repositories if you push. Enter your **Atlassian account email**. A token that is not an API token, such as an OAuth access token, needs no email.
4. Pick a repository from **Repositories GGX can access** and give it a **Name in GGX**.

## Notes

- GGX lists the repositories of the workspaces you belong to.
- Use **Disconnect my account** to remove your saved credentials.
