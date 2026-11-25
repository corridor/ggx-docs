---
title: "ServiceNow"
description: "Create and link ServiceNow incidents and other table records from GGX issues, with each person signing in to your ServiceNow instance."
---

[ServiceNow](https://www.servicenow.com/) is an IT service management platform. GGX uses it to turn issues found in annotation queues and feedback portals into ServiceNow records, usually incidents.

## What it does in GGX

- Create a record from a GGX issue (Issues Found), in a table you pick.
- Link an existing record by number (for example `INC0012345`) or URL.
- Show each linked record's state and refresh it in the background and on demand.
- Records are created as the person who signed in, with their ServiceNow roles.

## How to connect

1. A ServiceNow administrator with the `security_admin` role creates an **OAuth API endpoint for external clients** under **System OAuth**, then **Application Registry**, with the redirect URL shown by GGX. The refresh token lifespan must be above 0.
2. An administrator saves the **Instance URL**, **Client ID** and **Client secret** in **Org Settings → Integrations → Issue trackers → ServiceNow**.
3. Each person opens **My Account → Integrations → ServiceNow** and signs in.

## Notes

- **Tables** lists the tables a ticket can be created in or linked from, separated by commas or lines. It defaults to `incident`.
- **Default field values** is a JSON object of fields every new ticket gets, such as `{"category": "software"}`, for fields your instance requires. All values are strings, and a reference field takes a `sys_id`. GGX writes the short description and description itself.
- ServiceNow's Table API is off by default. Ask a ServiceNow administrator to activate its ACLs for each table, and to give the people who connect the roles to read and create records in them.
- GGX reads the label of a record's state. A label named like a GGX status counts as that status. The standard incident labels New, In Progress and On Hold count as Open, Resolved and Closed as Resolved, and Canceled as Won't fix. Other labels are shown as written.
