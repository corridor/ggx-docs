---
title: "Create a project"
description: "Describe a project and let Corra build it with agents, prompts, documents and data. Organization administrators only; shown with the prototypes."
---

**Create project with Corra AI (needs root mode)** builds a whole new project from a description. Corra writes the agents, prompts, documents and data, and builds the project in the background. Only an organization administrator can use it. Others get "Only an organization administrator can create a project with root mode."

:::note
This option is a prototype. It is offered only while the prototypes are shown, and the setting is not kept: reloading the page hides them again.
:::

## Start

1. In the project list, open the dialog to create a project.
2. Show the prototypes: right-click the search box and choose **Show Prototypes**.
3. Choose **Create project with Corra AI (needs root mode)**: "Describe the project and Corra builds it for you."
4. Fill in the form.

| Field | Meaning |
|-------|---------|
| **Name** | The new project's name. It must not match an existing project. |
| **What is the project about?** | Your description, up to 4,000 characters. |
| **Description (optional)** | A line for the project's home page. |
| **LLM** | The provider Corra builds with. |

5. Click **Create project**.

The run takes a few minutes. You can close the dialog. When the run ends, the project appears in the list. Click **Stop** to cancel; no project is created then. Only one run can work for you at a time. If the run fails, the form shows the reason.

## What Corra builds

Corra plans the folders and objects, writes them, checks them, and builds the project once. It refuses to build a project that is too thin, so the result has many agents with versions and descriptions rather than a single stub. The project is created under the usual rules for a new project.
