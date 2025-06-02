---
title: Collaboration
---

The platform has been designed in a way that enhances collaboration among teams in the development, testing and monitoring of various GenAi pipelines. The assets from various workstreams can be organized at a central location enabling developers, reviewers and testers to build, iterate, and reuse together.

## Requesting Object Access and Sharing Objects:

Registered objects in Draft/Pending Approval statuses can be shared with users on the platform or users can raise the access request.

There are currently two types of accesses (Read and Write) that can be requested or provided.

- **Read** - With Read access, the user can View, Run Evaluations, Download Documentation and Artifacts, and Reuse in another object.
- **Write**- With Write access, the user can Edit, Delete, Send for Approval, and Share with others.

When requesting access, the user can choose to request access to the object only or request access to the object along with its lineage.

Important Notes:

- Users can only request access to the objects they can potentially have access to based on the user role configuration in Settings.
- Re-sharing of objects with complete lineage is required if new objects are added to it.
- When an object is shared a notification is sent to the Receiver that an object has been shared.
- A Non-Owner will not be able to share the object if he/she has 'Read' permissions only.
- Users can also share access to objects using jupyter notebook using the Corridor package.
- Accesses granted through share can be changed/revoked by either the object owner or anybody with write access to the object.

## Access Management:

The Role-Based Access Management capability is available to govern how users, with a given role access, can use the platform. Every onboarded user on the platform is assigned a User Role.

Roles can be created based on the following framework:

- The platform is structured as a set of modules (Data Vault, GenAI Studio, Resources, etc.). The modules can be Enabled, Disabled or Hidden.
- Each module comprises different pages (e.g., Table Registry, Quality Procedure, Prompts, RAGs, Reports, etc.). The pages can be Enabled, Disabled or Hidden.
- Within each page, objects such as Tables, Models, Pipelines, and Reports can be accessed.
- Objects have properties and attributes on which access can also be controlled.
- Access can be of different types: read, write, approve, and superuser.
- Access to each of the above components can be granted independently using the Roles capability.

> **Note:** Granular access control can be given to roles (such as restricting access to a particular collection of objects) using custom rules.

## Integrate External Updates to Objects:

The registered object definition can be exported from the platform, modified externally, and re-synced using Corridor commands. The platform automatically tracks and records all external changes for clarity and consistency.

## Grouping Objects:

Groups provide a way to classify objects for control and display purposes. Groups are specific to object types.

- When defining Roles, Administrators can use groups to specify access rights. Different teams can create custom groups that are accessible only to the relevant team members to register, test and monitor their assets.
- In the registries objects are displayed by group thus making things easy to find and work on.

## Workspaces:

The platform enables the creation of multiple workspaces, allowing teams to work independently without visibility into each other's work.

## Monitoring Dashboard and Alerting:

The platform enables the creation of customized dashboards for key stakeholders and top management, providing a bird's-eye view of activities across different teams and stages of the application lifecycle.
