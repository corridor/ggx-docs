---
title: "Hive"
description: "Create and link Hive actions from GGX issues and keep their status in sync, with a personal API key an administrator allows."
---

[Hive](https://hive.com/) is a project management platform. GGX uses it to turn issues found in annotation queues and feedback portals into Hive actions.

## What it does in GGX

- Create a Hive action from a GGX issue (Issues Found), in a project you pick.
- Link an existing action by URL or ID.
- Show each linked action's status and refresh it in the background and on demand.

## How to connect

1. An administrator opens **Org Settings → Integrations → Issue trackers → Hive** and ticks **Let people connect with a personal API token**. Hive has no sign-in, so nobody can connect until this is on. A personal token acts as its owner, and Hive records what GGX does under that person.
2. Each person creates an API key from **My profile → API info** in Hive and pastes it in **My Account → Integrations → Hive**.
3. Optional: in the same dialog, an administrator can set another Hive server URL. Hive at `https://app.hive.com` works with nothing saved.

## Notes

- Statuses belong to the workspace's status library. To track them, add the five GGX statuses (Needs triage, Open, Resolved, Won't fix, Duplicate). Other statuses are shown as written.
- The description is sent as plain text.
