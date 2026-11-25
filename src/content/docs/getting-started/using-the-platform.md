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

The Learning Hub is a dialog with guided tours and recorded webinars. Open it from **Learning Hub** at the bottom of the sidebar, or from **Visit the Learning Hub** under **New around here?** on Home. The **Learning Hub** item in the profile menu opens the same dialog, but it appears only when your installation also has a Product Fruits workspace configured. Press Esc or click outside the dialog to close it.

### Sections

| Section | What it lists |
|---------|---------------|
| **Tracks** | Tours grouped by track. The built-in tracks are **Getting Started** (find your way around GGX), **How To Guides** (hands-on walkthroughs where you do the clicks, split into sub-headings) and **Learn Risk in AI** (why each control exists, shown on the real chatbot). Each track shows how many tours you have done and the minutes left. |
| **Search tours…** | Finds tours across all tracks by title, description or track name. |
| **Webinars** | Recorded sessions, each with its length in minutes. **Watch** opens the video in a new tab. **PDF** downloads the slides when a file is attached. |
| **Documentation** | A link to [docs.genguardx.ai](https://docs.genguardx.ai). |

Each tour row shows its steps and estimated minutes, and a **Start**, **Continue** or **Replay** button. **Start** is for a tour you have not finished. **Replay** appears after you finish it, and **Continue** marks the tour the **Up next** banner suggests. A tour that has no built-in walkthrough yet shows **Coming soon** with a locked button. The sidebar summary shows how many tours you have done across all tracks.

### Run a tour

1. In the Learning Hub, click **Start** on a tour. The dialog closes. Some tours switch to the project they use, or ask you to open a specific page first and tell you so if you are in the wrong place.
2. Most tours open with an intro screen. Click **Begin tour**, or **Explore on my own** to leave.
3. Follow the highlighted steps. **Continue** and **Back** move between steps. Some steps ask you to click the highlighted item yourself.
4. Click **Exit tour** at any time to stop.
5. At the end, a finish screen offers **Start next tour** or **Back to the Learning Hub**.

To restart a tour, open the Learning Hub and click **Start** or **Replay** on it. A tour you exit does not count as done, and exiting does not save your place, except for the required tour below.

GGX records each tour start and finish on the server against your user. That record decides which tours show as done, so your progress follows you across browsers.

The tour **Know your way around** is required. It starts automatically when you open Home until you complete it, has no **Explore on my own** option, and resumes from the step where you exited the next time you sign in. That resume position is stored in your browser.

### Where the content comes from

Tour titles, descriptions, tracks and webinars are rows in the GGX database, not an external Help Center. The tour steps themselves are built into the GGX web app. Webinar videos are links, hosted by Vimeo in the standard content, and the app fetches video thumbnails from Vimeo, so those need internet access from the user's browser. Which tours and webinars a given installation lists depends on what has been loaded into its database; the dialog shows **No Tours Available** or **No Webinars Available** when there are none. GGX has no screen for editing them.

### Turn it off

The Learning Hub is controlled by the `UI_CONFIGS__enableLearningHub` setting in the API configuration. It is off unless set to `True`. When it is off, the sidebar button and the Home link are hidden. The hub's endpoints apply no extra permission check beyond being signed in. The **Know your way around** tour check on Home is not tied to this setting.
