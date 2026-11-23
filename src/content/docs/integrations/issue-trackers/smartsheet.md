---
title: "Smartsheet"
description: "Create and link Smartsheet rows from GGX issues, using one service account access token saved by an administrator."
---

[Smartsheet](https://www.smartsheet.com/) is a spreadsheet-style work management tool. GGX uses it to turn issues found in annotation queues and feedback portals into rows of a sheet.

## What it does in GGX

- Create a row in a sheet from a GGX issue (Issues Found).
- Link an existing row by `<sheet ID>:<row ID>` or by the row's link (right-click a row, then **Get Row Link**).
- Show each linked row's status and refresh it in the background and on demand.
- The organization connects Smartsheet once with a service account. Nobody needs a Smartsheet sign-in of their own, and there is no Smartsheet card in My Account.

## How to connect

1. Use a service account: a user made for GGX with a license that can edit sheets. Signed in as that user, open **Account**, then **Personal Settings**, then **API Access**, and generate a new access token.
2. Create the sheet. Its primary column holds the title. Add a **Status** column of type Dropdown with options named Needs triage, Open, Resolved, Won't fix and Duplicate. Optionally add a **Description** column and a **GGX issue** column, both of type Text/Number.
3. Share the sheet with the service account as **Editor**.
4. An administrator opens **Org Settings → Integrations → Issue trackers → Smartsheet**, pastes the **API access token** and the **Sheet** (ID or link), and chooses **Check sheet**. GGX shows the columns it found and what is missing.

## Notes

- **Status column**, **Description column** and **Link column** name the columns GGX uses; they default to Status, Description and GGX issue. Without a description column GGX adds the description as a comment on the row.
- Without a Needs triage option, new rows get an empty status. An option with another name is shown as written and counts as unknown.
- The Europe, Australia and Government regions have separate tokens and hosts. Enter the host under **API host** and save it before using **Check sheet**.
- A project can use its own sheet in **Project Settings**.
