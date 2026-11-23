---
title: "ProdPad"
description: "Create and link ProdPad ideas from GGX issues and keep their status in sync, with a personal API key per person."
---

[ProdPad](https://www.prodpad.com/) is a product management tool. GGX uses it to turn issues found in annotation queues and feedback portals into ProdPad ideas.

## What it does in GGX

- Create a ProdPad idea from a GGX issue (Issues Found).
- Link an existing idea by number or URL.
- Show each linked idea's status and refresh it in the background and on demand.

## How to connect

1. Each person generates an API key in their ProdPad profile settings and pastes it in **My Account → Integrations → ProdPad**.
2. Optional: an administrator can set another ProdPad API URL in **Org Settings → Integrations → Issue trackers → ProdPad**.

## Notes

- ProdPad ideas are requests for a product team, not tickets for engineers. Use a defect tracker where you have one.
- To track status, create the five GGX statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) in the ProdPad workflow. Other statuses are shown as written. GGX reads status and does not change it in ProdPad.
