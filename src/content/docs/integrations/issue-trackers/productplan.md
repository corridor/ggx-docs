---
title: "ProductPlan"
description: "Send GGX issues to ProductPlan as Discovery ideas, with a personal API token an administrator allows."
---

[ProductPlan](https://www.productplan.com/) is a roadmapping tool. GGX can send an issue to ProductPlan as a Discovery idea.

## What it does in GGX

- Create a Discovery idea from a GGX issue (Issues Found).
- Link an existing idea by number.
- Show whether the idea is open (visible) or resolved (archived) and refresh it on demand.

## How to connect

1. An administrator opens **Org Settings → Integrations → Issue trackers → ProductPlan** and ticks **Let people connect with a personal API token**. ProductPlan has no sign-in, so nobody can connect until this is on. A personal token acts as its owner, and ProductPlan records what GGX does under that person.
2. Each person creates a token on the **custom integrations** page of ProductPlan and pastes it in **My Account → Integrations → ProductPlan**.
3. Optional: in the same dialog, an administrator can choose whether to send the person's name and email to ProductPlan as the idea's source. This is off by default.

## Notes

- ProductPlan ideas have only two states, visible and archived, so GGX cannot tell a resolved idea from a rejected one.
- GGX only reads the idea; changing a GGX status does not update ProductPlan. The idea is shown as its number, without a link.
- The description is sent as plain text.
