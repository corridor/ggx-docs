---
title: "Platform Settings"
description: "Reference for Org Settings, Advanced Settings in GGX: governance, execution environment, security limits, user onboarding email, update checks and backups."
---

**Advanced Settings** holds the organization-wide limits and defaults of the platform. Only users with the **Organization Admin** permission see it. Open **Org Settings**, then **System → Advanced Settings**. Change the values, then click **Save**, or **Cancel** to discard.

The **⋮** menu next to **Save** opens **Maintenance Scripts**, **Check for updates** and **Export Database**.

## Governance

| Setting | Effect |
|---------|--------|
| **Require Simulations** | Requires simulations to be attached to a review request. |
| **Allow Old Simulations** | Allows older simulations to be used when requesting approvals. |

Both are **Yes** or **No** choices. See [Approval Workflows](/evaluate-and-approve/approval-workflows/) for the review process.

### Relevant industries

Pick one or more of **Healthcare providers**, **Insurance payers**, **Banks**, **Credit unions** or **Other**. The setting records the industries that GGX serves for your organization. Every user can read it. Leaving it empty is allowed.

## Setup Execution Environment

| Setting | Use |
|---------|-----|
| **Environment Variables (.env)** | Paste `NAME=value` lines, one per line. Comments and quoted values work. Values are used as written, with no variable or shell expansion. They override integration variables and apply the next time an execution environment is set up. |
| **Python Environment Setup (optional)** | Python that runs before any analytics in a Python context, such as test sessions and helper tools. For example, `os.environ['EXAMPLE_VAR'] = 'val1'`. |

## Hooks

**Data Lake - Pre Read Hook** is extra Python that runs when GGX reads from a data lake. Use it to add validation or settings. The variable `location` holds the location being read and `username` holds the user reading it.

:::caution
Hooks change how core functionality works. Use them with care.
:::

## User onboarding

Set the **Email Subject** and the email body that GGX sends when you use **Resend Invitation Email** on a user. Use `{{ visible_name }}` and `{{ email }}` in the text to personalize it. See [Users and Teams](/administration/users-and-teams/).

## Security

| Setting | Effect |
|---------|--------|
| **Maximum File Size** | Largest file a user can upload, in MB. |
| **Maximum Job Records** | Largest number of records a job can run on. |
| **Default Execution Timeout** | Hours a job may run before it is stopped, when neither the user nor the project sets a limit. A project can set its own in its advanced settings. Leave empty to use the platform default of 2 hours. |
| **Allowed File Extensions** | Comma-separated list of extensions users may upload, for example `.txt, .csv, .pdf`. |
| **Allowed Python Imports** | Comma-separated list of modules that definitions may import when GGX tests their syntax, for example `numpy, pandas, os, re`. Empty means no restriction. See [Packages](/technology/self-hosting/configurations/packages/). |
| **Enable Telemetry** | When on, GGX captures anonymous usage statistics to improve the product. |

## Check for updates

Choose **⋮ → Check for updates**. GGX looks for an installer ZIP and compares it with the installed version.

- **No new version found** means the installed version is current.
- **New version found** shows the **Installed** and **Available** versions. Click **Install update** and confirm. The install replaces Python packages and restarts the services. A tag shows progress and ends as **Installed** or **Failed**. After a failure the environment may be partly changed. You can retry the install.
- **Manually upload an installer ZIP** adds an installer yourself.

If the database needs an upgrade after the install, the page says so.

## Export Database and file storage

Choose **⋮ → Export Database** to open the backup dialog.

- **Create New Backup** exports the database table by table, then starts a download. The dialog also lists the ten most recent backups you can download again.
- **Export File Storage** copies the files in GGX file storage to a folder you choose. Click **Choose Folder and Download**. New and changed files replace matching files, unchanged files are skipped, and local files are never deleted. You can pause and resume the transfer. Keep the page open while it runs.

Folder downloads need desktop Chrome or Edge over HTTPS (or localhost).

This is one part of a backup plan. See [Backups & Restore](/technology/self-hosting/scaling/backups/) for the rest.

## Related settings pages

- **Python packages** and **Integrations** (in the **System** group) are covered under [Self-hosting configuration](/technology/self-hosting/).
- [System Health](/administration/system-health/)
