---
title: "Jira Cloud"
description: "Create and link Jira Cloud tickets from GGX issues and keep their status in sync, with each person signing in with their Atlassian account."
---

[Jira Cloud](https://www.atlassian.com/software/jira) is Atlassian's issue and project tracker. GGX uses it to turn issues found in annotation queues and feedback portals into Jira tickets.

## What it does in GGX

- Create a Jira ticket from a GGX issue (Issues Found), in a project and site you pick, with an issue type.
- Link an existing ticket by key (for example `PROJ-123`) or URL.
- Show each linked ticket's status in GGX. Status is refreshed in the background and on demand with **Refresh**; changing it in Jira does not change the GGX issue automatically.
- Tickets are created as the person who connected, so Jira permissions apply.

## How to connect

1. Each person opens **My Account → Integrations → Jira Cloud** and signs in with their Atlassian account (OAuth 2.0). GGX uses the sites that Atlassian returns for that account.
2. By default GGX signs in with the official GenGuardX app. An administrator can instead register the organization's own Atlassian OAuth app in **Org Settings → Integrations → Issue trackers → Jira Cloud**, or remove it to return to the default.

## Notes

- The person needs **Browse Projects** and **Create Issues** in the Jira project, and permission to transition issues to see status changes.
- Jira Data Center and Server are not supported.
- Disconnecting keeps the linked tickets and their last known status, with updates paused until someone reconnects.
