---
title: "Organization Permissions"
description: "What the four GGX organization permissions allow, how to assign them to users and teams, and how they relate to project roles."
---

Project roles control what a person can do inside one project. Organization permissions sit above them and apply to every project. An administrator assigns them on a user or on a team.

## The four permissions

| Permission | What it allows |
|------------|----------------|
| **All Project Read** | View all projects and their content. |
| **All Project Write** | Everything in All Project Read, plus create and edit content across all projects. |
| **All Project Manage** | Read and write in all projects, plus manage project members, roles and other project-level settings. |
| **Organization Admin** | Manage organization-wide integrations, user permissions and other settings. |

A user with none of these gets access only through project roles, which is the usual case. In the user list this person shows as **Member**.

:::note
**Organization Admin** also unlocks the **System** group in Org Settings (**Python packages**, **Integrations**, **System Health**, **Advanced Settings**) and a user's **Activity** page.
:::

## Assign a permission

1. Open **Org Settings**, then **Users** (or **Teams**).
2. Open the user or team.
3. Under **Select permissions**, tick the permissions to grant.
4. Click **Save** (**Save Team** for a team).

A user gets the permissions set on their own record plus the permissions of every team they belong to. The user list shows the highest access a person has. Use the **Access** filter to find everyone with a given permission.

## Combine with project roles

- Use **project roles** to give people access to specific projects. See [Collaboration](/register-and-refine/collaboration/#access-management).
- Use **organization permissions** only for people who need the same access in every project, such as an auditor (All Project Read) or a platform owner (Organization Admin).

The **Projects overview** on a user's page lists each project the person can reach with their project roles. A project reached only through an organization permission shows **Organization-wide access** instead of a role.
