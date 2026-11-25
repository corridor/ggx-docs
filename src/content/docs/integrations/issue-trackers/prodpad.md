---
title: "ProdPad"
description: "Create and link ProdPad ideas from GGX issues and keep their status in sync, with a personal API key an administrator allows."
---

[ProdPad](https://www.prodpad.com/) is a product management tool. GGX uses it to turn issues found in annotation queues and feedback portals into ProdPad ideas.

## What it does in GGX

- Create a ProdPad idea from a GGX issue (Issues Found).
- Link an existing idea by number or URL.
- Show each linked idea's status and refresh it in the background and on demand.

## How to connect

1. An administrator opens **Org Settings → Integrations → Issue trackers → ProdPad** and ticks **Let people connect with a personal API token**. ProdPad has no sign-in, so nobody can connect until this is on. A personal token acts as its owner, and ProdPad records what GGX does under that person.
2. Each person generates an API key in their ProdPad profile settings and pastes it in **My Account → Integrations → ProdPad**.
3. Optional: in the same dialog, an administrator can set another ProdPad API URL.

## Notes

- ProdPad ideas are requests for a product team, not tickets for engineers. Use a defect tracker where you have one.
- To track status, create the five GGX statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) in the ProdPad workflow. Other statuses are shown as written. GGX reads status and does not change it in ProdPad.
