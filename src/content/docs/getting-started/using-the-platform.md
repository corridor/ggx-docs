---
title: "Using the platform"
description: "Switch projects, search for objects, follow background jobs, open Corra AI, read notifications, use Home and Project Home, and start the Learning Hub."
---

This page covers the parts of the GGX app that surround the sidebar: the header, the project switcher, Home and the Learning Hub. For the sidebar itself, see the [Platform tour](/getting-started/platform-tour/).

## Switch projects

Everything you open in GGX belongs to a project, and the app shows the project you have selected.

1. Click the project name. It is in the **PROJECT** box at the top of the sidebar, or in the header on Home and on the **Projects** page.
2. Optional: type in **Search projects** to filter by name or description.
3. Click a project.

If you are on a page that exists in the new project, GGX opens the same page there. Otherwise it opens the new project's **Project Home**. A project that is still being created shows a **Building…** tag.

Click **View all projects** at the bottom of the list to open the **Projects** page, which lists every project you can open and has a **Create** button for a new one. **All Projects** is shown as the name when no project is selected.

## Search

**Search** finds objects across GGX and opens them.

1. Press **Ctrl+K** (or **Cmd+K** on a Mac), or click **Search** in the header.
2. Type at least three characters in **Search Corridor…**. Before you type, the list shows **Recent Items**.
3. Pick a result, or use the arrow keys and press Enter. Hold Ctrl while you click to open the result in a new tab.

Each result shows its type icon, name, version, who created it and when, and its status. The panel's **Quick Actions** open a new object directly: **New Table**, **New Model** and **New Pipeline**.

## Background jobs

The clock icon in the header shows work that runs in the background. A badge with a number means jobs are running; its tooltip reads **Background jobs are running** or **No background jobs running**.

1. Click the clock icon. The **Background Jobs** popover lists how many jobs are **Running**, **Queued** or **Compiling**.
2. Click **More Info** for the full **Background Jobs** table. It shows the job name, object, status, run, compile and queue times, queue position, owner and description. Use the filters on the grid headers to narrow it.

The refresh control in the popover reloads the numbers. Finished jobs are reported through [notifications](#notifications).

## Corra AI

The sparkle button in the header opens **Corra AI**, the assistant built into GGX. A badge shows how many of its runs are working now.

The drawer lists your Corra AI runs and chats, newest first. Filter them with **All**, **Running**, **Runs** or **Chats**. Each entry shows its state, a progress line while it runs, and when it was last active. **Open** takes you to the object a run belongs to, and **Open chat** reopens a conversation. Click **New chat** to start a conversation. **Refresh** reloads the list.

## Notifications

The bell in the header shows a badge when you have unread notifications. Click it to open the list, which you can filter, search and star. Email notifications are separate and need setup by an administrator. See [Branding, Account and Notifications](/administration/branding-and-notifications/#notifications) for every control.

## Profile menu

On Home and **Projects**, the profile avatar is in the header. Inside a project it is at the bottom of the sidebar. Its menu has:

| Group | Items |
|-------|-------|
| **Support** | **Documentation** opens this site. **Learning Hub** appears when your installation has the hub set up for the profile menu. |
| **IDEs** | Shortcuts to the IDE integrations your administrator has connected. Shown only when there are any. |
| **Profile** | **Org Settings**, **My Account** and **Logout**. |

The **Profile** heading also has a button to switch between light and dark mode, and a key button that copies your API key when you have one. See [Administration](/administration/) for **Org Settings** and **My Account**.

## Home and Project Home

GGX has two home pages.

| Page | Address | What it shows |
|------|---------|---------------|
| **Home** | `/home` | Your assignments and the platform modules. It has no sidebar. |
| **Project Home** | `/<project-slug>` | The overview of one project: lifecycle stages, evidence and activity. See [Governance Oversight](/deploy-and-monitor/oversight/). |

### My work and Platform

Home has two views. If you have assignments, the switch at the top offers **My work** and **Platform**.

- **My work** shows each assignment as a card: feedback portals to test, annotation queues to label, issues assigned to you and approvals to decide. With nothing assigned it says **You're all caught up**, and **Visit the platform** switches to the Platform view.
- **Platform** shows one card per module you can access, each with a **Launch** button, and a **Recent Activities** panel. **Launch** opens that module in the last project you used. When you have assignments, the **Show my work** button returns to My work.

Without a saved choice, Home opens on **My work** if you have assignments, and on **Platform** if not. GGX remembers your choice in this browser. If you can open no modules in a project, Home shows a message to ask your administrator for access. See [Branding, Account and Notifications](/administration/branding-and-notifications/#home-my-work-and-platform) for the assignment list details.

Review-only users land on **My assignments** (`/assignments`) instead.

## Learning Hub

The Learning Hub holds guided tours and recorded webinars. It is available only when your administrator has turned it on. When it is on, open it from **Learning Hub** at the bottom of the sidebar or **Visit the Learning Hub** on Home.

The hub has these parts:

- **Tracks**: groups of tours. The built-in tracks are **Getting Started** (find your way around GGX), **How To Guides** (hands-on walkthroughs where you do the clicks) and **Learn Risk in AI** (why each control exists, shown on a real chatbot). Each track shows how many tours you have done and the minutes left.
- **Tours**: each has a **Start** button, which becomes **Continue** when you are partway and **Replay** when you have finished. An **Up next** banner suggests the next tour.
- **Search tours…**: finds tours by name across all tracks.
- **Webinars**: recorded sessions from the GGX team. **Watch** plays one, and **PDF** downloads its slides when available.
- **Documentation**: a link to this site.

The tour **Know your way around** starts automatically the first time, until you complete it.
