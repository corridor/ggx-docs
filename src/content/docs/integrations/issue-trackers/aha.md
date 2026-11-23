---
title: "Aha!"
description: "Create and link Aha! ideas from GGX issues and keep their status in sync, with a personal API key per person."
---

[Aha!](https://www.aha.io/) is a product management and roadmap tool. GGX uses it to turn issues found in annotation queues and feedback portals into Aha! ideas.

## What it does in GGX

- Create an Aha! idea from a GGX issue (Issues Found), in a product (workspace) you pick.
- Link an existing idea by reference number (for example `PRJ1-I-123`) or URL.
- Show each linked idea's status and refresh it in the background and on demand.

## How to connect

1. An administrator opens **Org Settings → Integrations → Issue trackers → Aha!** and saves the account subdomain (the part before `.aha.io`).
2. Each person creates an API key in their Aha! profile and pastes it in **My Account → Integrations → Aha!**.

## Notes

- Aha! is a product tool, so GGX issues become ideas, not defects. Features and requirements are not created.
- Idea statuses belong to the product's workflow. To track them, create the five GGX statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) in the idea workflow. Other statuses are shown as written.
