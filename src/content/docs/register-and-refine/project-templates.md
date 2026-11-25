---
title: "Project Templates"
description: "Start a GGX project from a ready-made template with agents, data, reports and a Code Repo, instead of an empty project."
---

A project template builds a complete project for a use case: agents, prompts, knowledge, feedback portals, monitoring, data, reports, risk assessments and a Code Repo. Use one to explore GGX with realistic content, or as a starting point for your own work.

## Create a project from a template

<ol>
<li>Open the projects page and click <strong>Create</strong>. The <strong>Start a new project</strong> window opens. On an organization with no projects yet, click <strong>Start from a template</strong> instead.</li>
<li>Pick a template. Templates are grouped by industry. Use the search box to find one by name, industry or topic. Selecting a template shows its summary, its industry and framework, and <strong>What's included</strong>.</li>
<li>Click <strong>Next</strong>.</li>
<li>Under <strong>LLM</strong>, choose the model provider the project's agents use: <strong>Anthropic</strong>, <strong>OpenAI</strong>, <strong>Google Gemini</strong>, <strong>AWS Bedrock (Anthropic)</strong> or <strong>Azure OpenAI</strong>.</li>
<li>Enter a <strong>Project name</strong> and an optional <strong>Description</strong>. The gear button opens <strong>Advanced options</strong>, where you can set an <strong>Organization name</strong>; otherwise the template's own name is used.</li>
<li>Click <strong>Create</strong>.</li>
</ol>

To start blank, choose **Create empty project** in the first step instead.

## While the project builds

GGX builds the project step by step and shows **Building your project…** with a progress bar and the current step. You can close the window: the project keeps building, everyone sees it in the list while it builds, and it opens from the list when ready.

If the build stops, for example because the server restarted, the window offers **Retry**, which removes the unfinished project and builds it again, or **Remove and go back**. If the build fails, the window shows the reason and a **Back** button.

## What's included

The **What's included** panel groups a template's contents under **Agents**, **Knowledge & skills**, **Feedback**, **Monitoring**, **Data & evaluations** and **Governance & risk**.

Each template also adds a [Code Repo](../inventory-management/#code-repos) that holds the template's agents as Python modules. The repository has a commit history that follows the versions of the agents, alongside the other commits a team makes, such as setup, fixes and merged branches. The code in the repository is written from the same definitions as the agents, prompts, models and RAGs in the project, so the two agree.

## Prototype templates

Some templates are marked as prototypes and are hidden by default. Right-click the search box and choose **Show Prototypes** to list them, or **Hide Prototypes** to hide them again.
