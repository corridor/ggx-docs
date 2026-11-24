---
title: "How GGX is organized"
description: "How GGX groups work into projects, how access is granted, and how the three lifecycle stages map to what you see in the app."
---

GGX organizes work in two ways. People and access are organized by **organization**, **teams** and **projects**. The work itself follows a lifecycle of three stages. This page explains both, then points to the page that covers each part in depth.

## The three lifecycle stages

Every GenAI solution in GGX moves through the same three stages.

| Stage | What happens | Start here |
|-------|--------------|------------|
| **Register & Refine** | Register datasets, models, prompts, RAGs and agents, then improve them version by version. | [Register & Refine](/register-and-refine/) |
| **Evaluate & Approve** | Test with evaluations and human reviewers, record risks, and get an approval decision. | [Evaluate & Approve](/evaluate-and-approve/) |
| **Deploy & Monitor** | Deploy the approved agent, watch it in production, and turn findings into new tests. | [Deploy & Monitor](/deploy-and-monitor/) |

The app's left sidebar is grouped by area of work rather than by stage, so the groups do not line up one to one. For example, **Deployments** sits under **Risk & Compliance** in the sidebar but belongs to Deploy & Monitor. The [Platform tour](/getting-started/platform-tour/) lists every sidebar item with the stage and page that cover it.

## Organization, teams and projects

| Level | What it is | Where you manage it |
|-------|------------|---------------------|
| **Organization** | Your whole GGX installation. It holds the users, teams, branding, integrations and platform settings shared by everyone. | **Org Settings** in the profile menu. See [Administration](/administration/). |
| **Team** | A group of users. A team can be given organization permissions, and can be added to a project with project roles. | **Org Settings**, **Teams**. See [Users and Teams](/administration/users-and-teams/). |
| **Project** | The workspace for one use case. Every dataset, model, prompt, RAG, agent, report, evaluation, risk assessment, approval, deployment, monitoring task and annotation queue lives in a project. | The project switcher in the header. Members and roles are under **Project Settings**. |

Objects belong to exactly one project. The sidebar always shows the contents of the project you have selected, and its name appears in the **PROJECT** box at the top of the sidebar.

## How access works

Two layers decide what a person can open.

1. **Project access.** Add users or teams to a project under **Project Settings → Project Members** and give each one or more project roles. A project's **General access** setting is either **Restricted** (only the users and teams you add can open it) or **Everyone in the organization** (anyone in the organization opens it with the role you pick). People who lack access can request it, and a project manager approves or rejects the request under **Pending Requests**.
2. **Organization permissions.** An administrator can give a user or team **All Project Read**, **All Project Write**, **All Project Manage** or **Organization Admin**. These apply in every project. See [Organization permissions](/administration/permissions/).

A project role controls which sidebar sections and pages the person sees, and what they can do with each type of object. If a section or page is missing from your sidebar, your role in that project does not include it. See [Collaboration](/register-and-refine/collaboration/#access-management) for how roles are built.

Each user also has a **user type**. A **Review-only user** lands on **My assignments** with a reduced menu, while a **Full user** lands on the full platform. See [User types](/administration/users-and-teams/#user-types).

## Where to go next

- [Platform tour](/getting-started/platform-tour/): every sidebar item, what it is for and where it is documented.
- [Using the platform](/getting-started/using-the-platform/): the project switcher, Search, background jobs, notifications, Home and the Learning Hub.
- [Administration](/administration/): users, teams, permissions and settings for administrators.
