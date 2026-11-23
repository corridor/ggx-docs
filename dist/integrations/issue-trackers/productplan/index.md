# ProductPlan
Source: https://docs.genguardx.ai/integrations/issue-trackers/productplan/
Markdown: https://docs.genguardx.ai/integrations/issue-trackers/productplan/index.md
Description: Send GGX issues to ProductPlan as Discovery ideas, with a personal API token per person.

[ProductPlan](https://www.productplan.com/) is a roadmapping tool. GGX can send an issue to ProductPlan as a Discovery idea.

## What it does in GGX

- Create a Discovery idea from a GGX issue (Issues Found).
- Link an existing idea by number.
- Show whether the idea is open (visible) or resolved (archived) and refresh it on demand.

## How to connect

1. Each person creates a token on the **custom integrations** page of ProductPlan and pastes it in **My Account → Integrations → ProductPlan**.
2. Optional: an administrator can choose in **Org Settings → Integrations → Issue trackers → ProductPlan** whether to send the person's name and email to ProductPlan as the idea's source. This is off by default.

## Notes

- ProductPlan ideas have only two states, visible and archived, so GGX cannot tell a resolved idea from a rejected one.
- GGX only reads the idea; changing a GGX status does not update ProductPlan. The idea is shown as its number, without a link.
- The description is sent as plain text.
