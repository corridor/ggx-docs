---
title: Collaboration
---

The platform is designed to enhance collaboration among teams involved in the development, testing, and monitoring of various GenAI pipelines. Assets from different workstreams can be organized in a central location, enabling developers, reviewers, and testers to build, iterate, and reuse together.

## Requesting Object Access and Sharing Objects:

Registered objects in Draft or Pending Approval status can be shared with users on the platform, or users can raise an access request.

There are currently two types of access (Read and Write) that can be requested or provided:

- **Read** – With Read access, the user can view, run evaluations, download documentation and artifacts, and reuse the object in another object.
- **Write** – With Write access, the user can edit, delete, send for approval, and share the object with others.

When requesting access, the user can choose to request access to the object only, or to the object along with its lineage.

Important Notes:

- Users can only request access to objects they are eligible for, based on the user role configuration in Settings.
- Re-sharing of objects with complete lineage is required if new objects are added to it.
- When an object is shared, a notification is sent to the receiver indicating that an object has been shared.
- A non-owner will not be able to share the object if they have 'Read' permissions only.
- Users can also share access to objects using Jupyter Notebook via the Corridor package.
- Access granted through sharing can be changed or revoked by either the object owner or anyone with write access to the object.

## Access Management:

Role-Based Access Management is available to govern how users, based on their assigned roles, can use the platform. Every onboarded user is assigned a user role.

Roles can be created based on the following framework:

- The platform is structured as a set of modules (Data Vault, GenAI Studio, Resources, etc.). Modules can be enabled, disabled, or hidden.
- Each module comprises different pages (e.g., Table Registry, Quality Procedure, Prompts, RAGs, Reports, etc.). Pages can be enabled, disabled, or hidden.
- Within each page, objects such as Tables, Models, Pipelines, and Reports can be accessed.
- Objects have properties and attributes on which access can also be controlled.
- Access can be of different types: read, write, approve, and superuser.
- Access to each of the above components can be granted independently using the Roles capability.

> **Note:** Granular access control can be given to roles (such as restricting access to a particular collection of objects) using custom rules.

## Integrating External Updates to Objects:

The registered object definition can be exported from the platform, modified externally, and re-synced using Corridor commands. The platform automatically tracks and records all external changes for clarity and consistency.

## Grouping Objects:

Groups provide a way to classify objects for control and display purposes. Groups are specific to object types.

- When defining roles, administrators can use groups to specify access rights. Different teams can create custom groups that are accessible only to the relevant team members to register, test, and monitor their assets.
- In the registries, objects are displayed by group, making them easier to find and work on.

## Workspaces:

The platform enables the creation of multiple workspaces, allowing teams to work independently without visibility into each other's work.

## Monitoring Dashboard and Alerting:

The platform enables the creation of customized dashboards for key stakeholders and top management, providing a bird's-eye view of activities across different teams and stages of the application lifecycle.
