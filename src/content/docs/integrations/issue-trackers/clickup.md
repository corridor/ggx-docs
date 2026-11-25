---
title: "ClickUp"
description: "Create and link ClickUp tasks from GGX issues and keep their status in sync, with each person signing in to ClickUp or using a personal API token."
---

[ClickUp](https://clickup.com/) is a work management platform. GGX uses it to turn issues found in annotation queues and feedback portals into ClickUp tasks.

## What it does in GGX

- Create a ClickUp task from a GGX issue (Issues Found), in a List you pick.
- Link an existing task by ID (for example `9hz`) or URL.
- Show each linked task's status and refresh it in the background and on demand.
- Tasks are created as the person who connected.

## How to connect

1. A ClickUp Workspace owner or admin creates an App in ClickUp (**Settings**, then **Apps**) and saves its client ID and client secret in **Org Settings → Integrations → Issue trackers → ClickUp**. The dialog shows the redirect URL to add in ClickUp.
2. Each person opens **My Account → Integrations → ClickUp**, signs in, and picks the Workspaces to share with GGX. ClickUp has no scopes.
3. Optional: an administrator can tick **Let people connect with a personal API token** in the same dialog. People can then paste a personal API token (it starts with `pk_`) from ClickUp under **Settings**, then **Apps**. This is off by default, because a personal token acts as its owner and does not expire.

## Notes

- GGX matches a task's status to its own issue statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) by name. To track them, create statuses with those names in the List. Other statuses are shown as written.
- If an administrator turns personal tokens off later, people connected with a token see a message asking them to reconnect with sign-in when they can.
