---
title: Approval Workflows
---

<helper-panel object='ApprovalWorkflow' location='list'>

## What is Approval Workflow?

After the development of GenAI pipelines, it is important to have a set of review processes to ensure various committees can collectively review and approve the pipeline. In Corridor, workflows that comprise multiple responsibilities can be created - and every responsibility is comprised of one or more reviewers. An object goes through the approval process from each of the responsibilities and reviewers.

## Why it is important?

- Creates an approval trail for model updates and changes.
- Provides clear documentation of who approved what and why.
- Ensures that only validated versions of models are deployed.
- Involves key stakeholders (developers, legal, compliance, business teams) in decision-making.
- Establishes clear ownership over AI pipeline governance.

## Registering Approval Workflows:

Approval workflows can be created and edited within the Settings section by anyone with the right authority level (mainly Admin and Master roles). Approval workflows are specific to object types.

1. Go to **Settings** and click on **Approval Workflow** Tab.
2. On the listing page click on the **Create** button to create a new one.
3. Fill in important details like **Name**, **Attributes** (Object Types, Description and Status).
4. Click on the **Create** button at the end to register the Approval Workflow.
5. Once registered the **Approval Workflow** can be edited to add responsibilities in the **Responsibilities** tab by clicking on the **Add New Responsibility** button.
6. Decide on **Veto and Editing power** to reviewers.
7. Select all the reviewers for the responsibility.
8. Add more responsibilities if required and **Save** to finally register the Approval Workflow.

> **Note:** The external tools option is available when third-party tools are configured and allows a third-party application to be defined as a responsibility within an approval workflow.

Once registered the Approval Workflow can be chosen while registering any object. This would ensure that the model goes through a proper approval process from all the responsibilities and reviewers before getting approved for production usage.

</helper-panel>

## Keeping track of Findings/Limitations

Once an object is approved, it is locked. No further changes can be made to it. But sometimes, reviews are done with findings or limitations on the usage and need follow-ups.

Corridor provides a flagging capability that can be used to Flag an Object (Even Post Approval) and can be created by anyone with Write access to Settings.
An object can be flagged for any reason (e.g. `NeedShadowResultsFor2Months` or `NeedRetrainIn6Months`) by any member of any Workflow that oversees objects of the same type. Similarly, a flag can be dropped (i.e., deactivated) by anyone with the authority to add the flag.

Once the flag is activated, a warning flag appears beside the object's name on the details page, indicating that the object and its assigned flags should be carefully reviewed before being used in downstream applications.
