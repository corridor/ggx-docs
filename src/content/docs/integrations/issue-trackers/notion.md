---
title: "Notion"
description: "Create and link Notion pages from GGX issues as rows of a database, with one integration token saved by an administrator."
---

[Notion](https://www.notion.so/) is a workspace for docs and databases. GGX uses it to turn issues found in annotation queues and feedback portals into pages of a Notion database.

## What it does in GGX

- Create a page in a database from a GGX issue (Issues Found).
- Link an existing page by URL.
- Show each linked page's status and refresh it in the background and on demand.
- The organization connects Notion once. Nobody needs a Notion account of their own, and there is no Notion card in My Account.

## How to connect

1. A Notion workspace owner creates an internal integration named GenGuardX (**Settings**, then **Integrations**) with the capabilities GGX lists in the setup guide, and copies its token.
2. Create the database. It needs a title column, a **Status** column of type Status or Select, and optionally a **Description** column of type Text and a **GGX issue** column of type URL.
3. In Notion, open the database, choose the three dots, then **Connections**, and add GenGuardX. A page you link must be shared with the integration too.
4. An administrator opens **Org Settings → Integrations → Issue trackers → Notion**, pastes the **Integration token** and the **Database** (ID or link), and chooses **Check database**. GGX shows the columns it found and what is missing.

## Notes

- **Status column**, **Description column** and **Link column** name the columns GGX uses. They default to Status, Description and GGX issue. Without a description column the description is written into the page; without a link column the link is the first line of the page.
- A project can use its own database in **Project Settings**.
- Pages are created through the one integration, not as the person who raised the issue.
