---
title: "Zoho Sprints"
description: "Create and link Zoho Sprints items in a project backlog from GGX issues, with each person signing in to their Zoho account."
---

[Zoho Sprints](https://www.zoho.com/sprints/) is Zoho's agile project tool. GGX uses it to turn issues found in annotation queues and feedback portals into items in a project's backlog.

## What it does in GGX

- Create an item from a GGX issue (Issues Found), in the backlog of a project of a team you pick.
- Link an existing item by key (for example `PRJ-I12`) or by its address in Zoho Sprints.
- Show each linked item's status and refresh it in the background and on demand.
- Items are created as the person who connected.

## How to connect

1. An administrator opens the Zoho API Console of their data center (for example `api-console.zoho.com`, or `api-console.zoho.eu` in Europe), adds a **Server-based Applications** client named GenGuardX, and adds the authorized redirect URI shown by GGX.
2. They choose the **Zoho data center** and save the client ID and client secret in **Org Settings → Integrations → Issue trackers → Zoho Sprints**. A Zoho token works in one data center only. People who connected before the data center changed must connect again.
3. Each person opens **My Account → Integrations → Zoho Sprints** and signs in.

## Notes

- The account that connects must be allowed to read the team and to add items to the project.
- GGX matches an item's status to its own issue statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) by name. Name statuses like these in the workflow of each project that gets items. Another status is shown as written and counts as open, in progress or done by its Zoho status type when Zoho gives one, and as unknown otherwise.
