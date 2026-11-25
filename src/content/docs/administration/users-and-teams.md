---
title: "Users and Teams"
description: "Create and invite GGX users, choose their user type, reset passwords, deactivate accounts, group people into teams and read a user's activity."
---

Manage people under **Org Settings**, **Access Management**. People with write access to these pages can create and change users and teams. Everyone else can view them.

## Users

**Users** lists every account. Search by name, or narrow the list with the filters:

| Filter | Options |
|--------|---------|
| Show users | **All users**, **Active**, **Inactive** |
| **Team** | One of your teams. Shown only when teams exist. |
| **Access** | The [organization permissions](/administration/permissions/), or **Member**. |
| **User type** | **Full user** or **Review-only user**. |

The sort button orders the list by **Name**, **Last active** or **Access**. **Clear filters** resets them.

### Create a user

1. Click **Create**.
2. Fill in the form:

   | Field | Notes |
   |-------|-------|
   | **Email** | The user's main email address. |
   | **Username** | The user's login name. |
   | **First Name**, **Last Name**, **Department** | Profile details. |
   | **Is Active** | Clear it to deactivate the account. |
   | **Additional Emails** | Extra addresses that can be used only to sign in. |
   | **User type** | See [User types](#user-types). |
   | **Select permissions** | See [Organization permissions](/administration/permissions/). |

3. Click **Create**.

After saving, add the person to projects under **Project Settings → Project Members**. See [Collaboration](/register-and-refine/collaboration/#access-management).

### Invite, reset a password or deactivate

Open a user, then use these controls:

- **⋮ → Resend Invitation Email** sends the invitation again. It uses the template in [Platform settings](/administration/platform-settings/#user-onboarding). If no subject or template is set, GGX refuses to send and asks you to configure it.
- **⋮ → Reset Password** sets a new password for the user. Enter it in **Password** and **Confirm Password**, then click **Confirm**.
- Clear **Is Active** and click **Save** to deactivate the account. Tick it again to reactivate.

You cannot edit your own username. Ask an administrator to change it.

### User types

The **User type** controls what a person lands on. It does not change what they can open: project roles and permissions still decide that.

| Type | What the person sees |
|------|----------------------|
| **Full user** | Organises the work, builds agents and checks that things work. Lands on the full platform. An empty type counts as Full user. |
| **Review-only user** | Comes to GGX to review what is assigned to them. Lands on **My assignments** and sees a reduced menu. |

Use Review-only for stakeholders who only approve agents, test in feedback portals, label annotation queues or handle issues. They see their work as a list, and a link opens the full platform when their access allows it.

### User activity

A user's page has an **Activity** button. An organization admin can open it for any user, and a user can open their own. Choose a period (**Last week**, **Last month**, **Last 3 months** or **All time**; days are in UTC). The page shows counts of **Logins**, **Runs**, **Objects saved**, **Messages sent** and **Approvals**, and a tab for each of **Logins**, **Runs**, **Building**, **Feedback & testing** and **Access**. **Export** downloads the data, and its menu offers **Download as JSON**.

## Teams

A team gives the same organization permissions to a group of people.

1. Open **Teams** and click **Create**.
2. Enter a **Team Name** and an optional **Description**.
3. Under **Assigned Users**, pick the members.
4. Under **Select permissions**, tick the [organization permissions](/administration/permissions/) the team grants.
5. Click **Create Team**.

To remove a team, open it, choose **⋮ → Delete Team** and confirm. A user's page lists their teams under **Teams overview**.
