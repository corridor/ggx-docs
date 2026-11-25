---
title: "Slack"
description: "Post each new GGX issue into a Slack channel with a bot token, and keep comments, status changes, and linked tickets in the same thread."
---

[Slack](https://slack.com/) is a team chat tool. GGX posts issues found in annotation queues and feedback portals into a Slack channel and continues in the same thread. See [Issue channels](../) for what is posted.

## What it does in GGX

- Post the first message of each new issue in the channel, then reply in its thread for comments, status changes, assignment, and linked tickets.
- Update the status line of the first message when the status changes.
- Use a default channel for the organization, with an optional channel per project.

## How to connect

1. In Slack, open `api.slack.com/apps`, choose **Create New App**, then **From scratch**. Name it GenGuardX and pick your workspace.
2. Under **OAuth & Permissions**, add these Bot Token Scopes: `chat:write`, `channels:read`, and `groups:read`. `chat:write.public` is optional.
3. Choose **Install to Workspace** (a workspace admin may have to approve it) and copy the **Bot User OAuth Token**. It starts with `xoxb-`.
4. An administrator opens **Org Settings → Integrations → Issue trackers → Slack**, pastes the token in **Bot token**, and chooses **Check token**. GGX shows the workspace name, and lists any missing scopes.
5. Under **Default channel**, search for a channel by name or type a channel ID such as `C0123456789`, and choose it. Choose **Send test message** to confirm.
6. Invite the bot to the channel: in Slack, send `/invite @GenGuardX`. Private channels need this before they appear. Public channels need it unless you added `chat:write.public`.

## Notes

- The token is stored encrypted and is never shown again. Leave the field empty to keep the saved one.
- Leave token rotation off in the Slack app. GGX stores one token and does not refresh it. If the token stops working, reinstall the app and save the new token.
- A project can choose its own channel in **Project Settings → Integrations → Slack**.
