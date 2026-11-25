---
title: "Asana"
description: "Create and link Asana tasks from GGX issues and keep their status in sync, with each person signing in to Asana or using a personal access token."
---

[Asana](https://asana.com/) is a work management platform. GGX uses it to turn issues found in annotation queues and feedback portals into Asana tasks.

## What it does in GGX

- Create an Asana task from a GGX issue (Issues Found), in a project you pick.
- Link an existing task by ID or URL.
- Show each linked task's status and refresh it in the background and on demand.
- Tasks are created as the person who connected.

## How to connect

1. An administrator creates an app in the Asana developer console (`app.asana.com/0/my-apps`), adds the redirect URL shown by GGX under **OAuth**, chooses **Full permissions**, and makes the app available in the Workspaces whose people will connect (**Manage distribution**). They save the client ID and client secret in **Org Settings → Integrations → Issue trackers → Asana**. Leave **Asana URL** empty unless Asana gave your organization another host.
2. Each person opens **My Account → Integrations → Asana** and signs in with Asana.
3. Optional: an administrator can tick **Let people connect with a personal API token** in the same dialog. People can then paste a personal access token from the Asana developer console. This is off by default, because a personal token acts as its owner.

## Notes

- A task is open or completed, shown in GGX as Open and Resolved. To use the other GGX statuses, add a single-select custom field named **Status** to the project with options named Needs triage, Open, Resolved, Won't fix and Duplicate. An option that disagrees with the completed box is ignored.
