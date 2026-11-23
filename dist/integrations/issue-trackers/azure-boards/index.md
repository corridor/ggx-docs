# Azure Boards
Source: https://docs.genguardx.ai/integrations/issue-trackers/azure-boards/
Markdown: https://docs.genguardx.ai/integrations/issue-trackers/azure-boards/index.md
Description: Create and link Azure Boards work items from GGX issues and keep their status in sync, with a personal access token per person.

[Azure Boards](https://azure.microsoft.com/products/devops/boards) is the work tracking service of Azure DevOps. GGX uses it to turn issues found in annotation queues and feedback portals into work items.

## What it does in GGX

- Create a work item from a GGX issue (Issues Found) in an Azure DevOps project, choosing one of the project's work item types (Bug, Task, Issue, User Story, and so on).
- Link an existing work item by number or URL.
- Show each linked item's status and refresh it in the background and on demand.
- Works with Azure DevOps Services and Azure DevOps Server.

## How to connect

1. An administrator opens **Org Settings → Integrations → Issue trackers → Azure Boards** and saves the organization URL (for Services, `https://dev.azure.com/<organization>`). The REST API version is optional and defaults to 7.1.
2. Each person creates a personal access token in Azure DevOps for that organization, with **Work Items: Read & write** and **Project and Team: Read**, and pastes it in **My Account → Integrations → Azure Boards**.

## Notes

- Work item states belong to the project's process. GGX matches the status of a ticket to its own issue statuses (Needs triage, Open, Resolved, Won't fix, Duplicate) by name, and shows any other status as it is written in the tracker. A state that Azure DevOps categorizes as proposed, in progress, or completed is counted accordingly.
- When a token expires, the person is asked to connect again and updates for their tickets pause until they do.
