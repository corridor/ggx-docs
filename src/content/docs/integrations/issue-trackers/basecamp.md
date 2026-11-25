---
title: "Basecamp"
description: "Create and link Basecamp to-dos from GGX issues, with each person signing in to their Basecamp 3 or Basecamp 4 account."
---

[Basecamp](https://basecamp.com/) is a project management tool from 37signals. GGX uses it to turn issues found in annotation queues and feedback portals into to-dos.

## What it does in GGX

- Create a to-do from a GGX issue (Issues Found), in a to-do list of a project you pick.
- Link an existing to-do by ID or URL.
- Show each linked to-do's status and refresh it in the background and on demand.
- Works with Basecamp 3 and Basecamp 4. A person in several Basecamp accounts can use them all.

## How to connect

1. An administrator signs in at `launchpad.37signals.com/integrations` and registers a new application named GenGuardX, choosing Basecamp 4 (or 3) and adding the redirect URI shown by GGX.
2. They save the **Client ID**, **Client secret** and a **Contact for Basecamp** (an email address or web address) in **Org Settings → Integrations → Issue trackers → Basecamp**. GGX sends the contact in the User-Agent of its requests, and Basecamp refuses requests without one.
3. Each person opens **My Account → Integrations → Basecamp** and signs in.

## Notes

- A to-do is open or completed, shown in GGX as Open and Resolved. To use the other GGX statuses, name to-do lists Needs triage, Open, Resolved, Won't fix and Duplicate. A list name applies only when it agrees with the completed box.
- An archived or trashed to-do is shown as such and counts as unknown.
