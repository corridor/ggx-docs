---
title: "Python packages"
description: "Add, update and remove the Python packages and package indexes that code in GGX runs with, for the whole organization or for one project."
---

The **Python packages** page controls which Python libraries are available to the code that runs in GGX: scoring logic, code runs, simulations and similar jobs. It also sets the package indexes GGX searches. The same page exists at two levels.

| Level | Where | Who sees it | Who can change it |
|-------|-------|-------------|-------------------|
| **Organization** | **Org Settings → System → Python packages** | Users with the **Organization Admin** permission (the **System** group is shown only to them). | Users with the **Organization Admin** permission. |
| **Project** | **Project Settings → Python packages** | Everyone who can open the project. | Users with **All Project Manage**, or a project role that has project settings access. |

The organization page is described in the app as "Manage Python packages inherited by all projects". The project page reads "Add Python packages to this project environment. Used by code runs and simulations."

The page shows the Python version of the environment as a tag next to the title.

## Find a package

- Type a name in **Search packages, for example openai or numpy…** and click **Search**. GGX searches the configured indexes and shows the number of matching packages. Results are paged 25 at a time. Click **Clear search** to go back to the recommended list.
- Without a search, the list shows recommended packages for AI and data workflows.
- Filter by status with **All**, **Added** or **Not Added**.
- Filter by category: **All**, **Agent Building**, **Model SDKs**, **Tools**, **Eval Toolkits**, **Data Connectors**, **Guardrails** and **Vector Stores**. A new search resets the category to **All**.
- Use **Sort by** to order the list by **Recommended** or **A to Z**.

Each row shows the package name, its summary and, for an added package, its version, an **Added** tag and any extras. If the index returns no summary, the row shows "Summary unavailable from this index."

## Add a package

1. Find the package.
2. Click **Add** on its row. GGX adds the latest version the index offers.
3. To pick another version, open the row's options menu (the ellipsis) and choose **Install another version**, or click the package name. The dialog lists **Available versions** with their release dates. Use **Find a version** to filter the list, and **Hide prereleases** to leave out prereleases. Click **Add** next to the version you want.

Versions marked **Yanked** cannot be added. A version marked **Prerelease** can. The version that is already added shows an **Added** tag. Choosing another version of an added package replaces the current one and keeps its extras.

Before saving, GGX resolves the package together with every other package of the environment. If the packages conflict, nothing is saved and a **Could not update dependencies** box shows the resolver's message. Click **Dismiss** to close it.

At the organization level, GGX checks the resolution against every project. It refuses the change when a project has selected a different version or different extras of the same package. Resolve that project first.

The options menu also offers **Open in PyPI** for packages found on `https://pypi.org/simple/`.

## Remove a package

Click **Remove** on the row of an added package. The row shows **Remove** only for packages that belong to the level you are on. See [Inheritance](#organization-and-project-inheritance).

## Update packages

At the project level, **Update All** appears once the project has packages of its own. It is disabled while another operation is running.

1. Click **Update All**. The **Update packages** dialog looks up the latest releases of the installed packages.
2. Review the list. Each row shows the package and the change, such as `1.2.0 → 1.4.1`. The dialog lists the newest releases that work together with the rest of the project's environment. Use the search box or the select-all checkbox to choose updates.
3. Click **Apply** with the number of selected updates, for example **Apply 3 updates**.

If every package is already at the newest compatible release, the dialog says so. If the look-up fails, the dialog shows **Could not look for updates** with the error and a **Try again** button. If applying fails, it shows **Could not apply the updates** with the error.

Only the project's own packages are updated. Organization packages stay as they are and are managed in Org Settings. The **Update All** button does not exist at the organization level.

## Package indexes

Click **Indexes** to open the **Package indexes** dialog. GGX searches indexes in the order listed.

1. Enter the address in **Index URL**, for example `https://pypi.org/simple/`.
2. Click **Add**.

GGX accepts only HTTP or HTTPS addresses, without credentials in the URL and without a query string. Otherwise it reports "Enter an HTTP or HTTPS index URL without embedded credentials or query strings". It adds a trailing slash to the address.

Click **Remove** next to an index to delete it. Indexes inherited from the organization show "Inherited from organization" and cannot be removed in a project. When the list is empty, the dialog says "No indexes configured. Add an index to discover and resolve packages."

## Import, export and warm the cache

Open the menu next to **Indexes** (**Dependency file options**).

| Entry | What it does |
|-------|--------------|
| **Warm cache** | Downloads and installs the configured packages now, so the first run does not wait for them. It can take a few minutes. A success message shows how many requirements were installed. If there are no packages, or the install fails, GGX shows an error. |
| **Download uv.lock**, **Download requirements.txt** | Downloads the environment as a lock file or a requirements file. |
| **Import requirements.txt**, **Import uv.lock** | Reads a file of at most 2 MiB and opens an **Import** dialog that previews the changes. Packages that the file does not list are kept. Click **Import dependencies** to apply. Conflicts are shown in red and block the import. |

## Organization and project inheritance

- A project's environment is the organization's packages plus the project's own packages. Package indexes work the same way: the organization's indexes come first, followed by the project's.
- In a project, a package from the organization shows an **Inherited** tag instead of **Remove**. Its tooltip says "Inherited from your organization. Manage this package in organization settings."
- A project cannot add or change a package that the organization already installs. GGX reports "This package is installed at Org Level and cannot be changed in Project Settings".

## What happens to running work

Code runs in an environment built from the package list and indexes that apply to its project, and GGX identifies each environment by that list. A change to the list therefore selects a different environment the next time code runs. Use **Warm cache** after a large change so the next run does not wait for the install.

## Drivers for data sources

Data sources such as Snowflake or PostgreSQL need a client package. See [Install the driver](/integrations/data-warehouses/data-sources/#install-the-driver) for the package each source needs.

## Related pages

- [Administration](/administration/)
- [System Health](/administration/system-health/)
- [Permissions](/administration/permissions/)
