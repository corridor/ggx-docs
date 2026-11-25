---
title: "Rally"
description: "Create and link Rally defects, user stories, and tasks from GGX issues and keep their state in sync, with a personal API key an administrator allows."
---

[Rally](https://www.broadcom.com/products/software/value-stream-management/rally) is Broadcom's agile planning and tracking tool. GGX uses it to turn issues found in annotation queues and feedback portals into Rally items.

## What it does in GGX

- Create a Rally defect or user story from a GGX issue (Issues Found), in a project you pick.
- Link an existing item by FormattedID (for example `DE123` or `US45`) or URL.
- Show each linked item's state and refresh it in the background and on demand.

## How to connect

1. An administrator opens **Org Settings → Integrations → Issue trackers → Rally** and ticks **Let people connect with a personal API token**. Rally has no sign-in, so nobody can connect until this is on. A personal token acts as its owner, and Rally records what GGX does under that person.
2. Each person creates an API key with write access on the **API Keys** page of their Rally account and pastes it in **My Account → Integrations → Rally**. Your subscription administrator must allow API keys.
3. Optional: in the same dialog, an administrator can set another Rally server URL or API version. Rally in the cloud at `https://rally1.rallydev.com` works with nothing saved.

## Notes

- Rally in the cloud (SaaS) is supported; Rally on-premises is not.
- States belong to the workspace. GGX matches the status of a ticket to its own issue statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) by name, and shows any other status as it is written in the tracker.
- Creating a task usually needs a parent item that GGX does not set; link an existing task instead.
