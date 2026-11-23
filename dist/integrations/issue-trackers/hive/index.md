# Hive
Source: https://docs.genguardx.ai/integrations/issue-trackers/hive/
Markdown: https://docs.genguardx.ai/integrations/issue-trackers/hive/index.md
Description: Create and link Hive actions from GGX issues and keep their status in sync, with a personal API key per person.

[Hive](https://hive.com/) is a project management platform. GGX uses it to turn issues found in annotation queues and feedback portals into Hive actions.

## What it does in GGX

- Create a Hive action from a GGX issue (Issues Found), in a project you pick.
- Link an existing action by URL or ID.
- Show each linked action's status and refresh it in the background and on demand.

## How to connect

1. Each person creates an API key from **My profile → API info** in Hive and pastes it in **My Account → Integrations → Hive**.
2. Optional: an administrator can set another Hive server URL in **Org Settings → Integrations → Issue trackers → Hive**. Hive at `https://app.hive.com` works with nothing saved.

## Notes

- Statuses belong to the workspace's status library. To track them, add the five GGX statuses (Needs triage, Open, Resolved, Won't fix, Duplicate). Other statuses are shown as written.
- The description is sent as plain text.
