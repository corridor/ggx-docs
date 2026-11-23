---
title: "monday dev"
description: "Create and link monday.com items on a monday dev board from GGX issues, with each person signing in to monday or using a personal API token."
---

[monday dev](https://monday.com/dev) is monday.com's product for software teams. GGX uses it to turn issues found in annotation queues and feedback portals into items on a board.

## What it does in GGX

- Create an item from a GGX issue (Issues Found), on a board you pick.
- Link an existing item by ID or URL.
- Show each linked item's status and refresh it in the background and on demand.
- Items are created as the person who connected.

## How to connect

1. An administrator creates an app in the monday **Developer Center** (profile menu, then **Developers**), adds the redirect URI shown by GGX under **OAuth**, and selects the scopes GGX lists (including `boards:write`). They save the client ID and client secret in **Org Settings → Integrations → Issue trackers → monday dev**.
2. Each person opens **My Account → Integrations → monday dev** and signs in with monday.
3. Optional: an administrator can tick **Let people connect with a personal API token** in the same dialog. People can then paste a personal API token from monday (**Developers**, then **My access tokens**). This is off by default, because a personal token acts as its owner and does not expire.

## Notes

- The same dialog has optional settings: **Status column** (the column whose labels are the status; the first status column of each board when empty), **Group for new items** (the top group when empty; every board you create items on needs a group with this name), **Workspace IDs** (limit which boards are listed) and **API host (advanced)**.
- A status label named like a GGX status (Needs triage, Open, Resolved, Won't fix, Duplicate) counts as that status. Another label counts as done when monday marks it as done, and as unknown otherwise.
