---
title: "Branding, Account and Notifications"
description: "Set your organization's name and logo, manage your own GGX account and API key, read in-app notifications and use the Home page assignment view."
---

## Branding

**Branding** sets the name and logo in the GGX header. Without them, the header shows GenGuardX. Everyone can read the page. Only an organization admin can change it.

1. Open **Org Settings**, then **Organization → Branding**.
2. Enter a **Name** (up to 100 characters). It appears next to the logo.
3. Click **Upload logo**. Use PNG, JPEG, WebP or SVG, up to 2 MB.
4. Optional: click **Upload logo for dark pages** if the main logo is hard to read on a dark background. Without it, GGX uses the same logo.
5. Check the **Preview**, which shows **On a light page** and **On a dark page**.
6. Click **Save**.

Use **Replace logo** or **Remove** to change a logo later. GGX removes scripts from SVG files before it uploads them.

## My Account

Every user has **My Account**, under **Org Settings → Account**. It has four parts:

- **Personal Details**: first name, last name, title and department. Click **Edit**. An administrator sets your username and permissions.
- **Preferences**: the **Color scheme**.
- **Account Security**: **Update** your email and, when password login is on, your password. The **API Key** row creates (**Create**), copies and regenerates your key. **How to use** explains how to use it from a notebook or IDE. The key carries the same permissions as your login, so keep it confidential. See [CI/CD and Direct to Production](/deploy-and-monitor/direct-to-production/).
- **Integrations**: your personal connections to GitHub and Jira, plus other Git or tracker accounts your administrator has set up. If one says it is not set up, an administrator has to configure it in **Org Settings → Integrations** first.

## Notifications

GGX tells you about events in two ways:

- **In the app**: the bell in the header shows a badge when you have unread notifications. Open it to see the list.
- **By email**, when your administrator has set it up. See [Email Notifications](/technology/self-hosting/configurations/notifications/).

In the notification list:

- Switch between **All**, **Read**, **Unread** and **Starred**.
- Filter by event: **Jobs**, **Approval** or **Monitoring Alert**, or by object type. **Search…** finds a notification, and **Clear Filters** resets the filters.
- Tick notifications, then use **Mark as Read** or **Mark as Unread**.
- Click the star on a notification to keep it under **Starred**.
- Sort with the **Date** button.

## Home: My work and Platform

When you have assignments, **Home** opens on **My work**. Assignments are feedback portals to test, annotation queues to label, issues assigned to you and approvals to decide. Each card shows its type, title, what to do, progress and due date. Overdue cards come first, then those due soon. Click **Show all** or **Show fewer** to expand the list. With nothing assigned you see **You're all caught up**.

The **My work** and **Platform** switch changes the view. **Platform** shows the modules and activity panels. GGX remembers your choice in this browser.

Review-only users land on **My assignments** instead. See [User types](/administration/users-and-teams/#user-types).

When the Learning Hub is turned on for your installation, **Visit the Learning Hub** on Home opens its guided tours.
