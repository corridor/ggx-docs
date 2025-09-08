---
title: Performance Tracking
---

## Overview

The Metrics Dashboard is a crucial component of the Monitoring Dashboard, providing users with valuable insights into the performance metrics of various objects on the platform.

### Populating Metrics Dashboard With Data

- To populate the Metrics Dashboard with recurring simulations for objects on the platform, users need to follow these steps:
- Go to the approved Object's page and navigate to the Jobs tab.
- For each row in the Jobs table, an action link labelled "Select for Metrics MD" will be visible under specific conditions:

  - The job must be the Iteration0 of a recurring job (only iteration 0 has this button)
  - There should be at least two iterations left to be completed in the recurring job
  - The job can be of any type (Simulation, Comparison, Validation, etc.)
  - The job should not be marked as "old"

**Note**: Users are allowed to select jobs run by other individuals, enabling stakeholders to leverage this capability as needed.

### Unselecting a Job

- To unselect a previously selected job, follow these steps:

  - Go to the approved Object's page and access the Jobs Tab
  - Find the Iteration0 of the recurring job that was previously selected and click on the action link "Unselect Job for MD."
  - Confirmation popup will appear. Upon confirmation, the job will no longer be tracked in the Metrics Dashboard.

### Selecting Another Job (When a Job Was Previously Selected)

- To select another job when a job was previously chosen, follow these steps:
- Go to the approved Object's page and access the Jobs Tab.
- For each row in the Jobs tab, observe the following conditions:

  - If there is no action link for MD, the job is not eligible based on the criteria mentioned earlier
  - If the action link "Select for Metrics MD" is shown, the job is eligible for selection
  - If the action link "Unselect Job for MD" shows, the currently selected row corresponds to the job previously chosen.

- Click on "Select for Metrics MD" for the job you wish to select.
- Upon confirmation, the newly selected job will be used to track the object in the Metrics Dashboard.

### Tracking Metrics and Handling Job Iterations

- Users can continue tracking metrics with recurring simulations. When job iterations end:
- Before job completion, notifications/emails can be sent to warn that there is only one iteration left.
- Upon job tracking completion, additional notifications/emails can be sent.
- After job completion:

  - If a user selects a new recurring job, it will be used from the time the new job was selected
  - If a user unselects the current recurring job, it will be stopped from the time the job was selected
  - If a user takes no action, the last iteration will continue to be shown in the Metrics Dashboard.

### Metrics Display and Thresholds

- The Metrics Dashboard will exclusively showcase the latest completed job selected by the user.

- There won't be a default base view, ensuring that the dashboard remains streamlined and focused on user preferences.

- Only the metrics registered through the UI for the specific object will be presented.

**Note**: The thresholds utilized on the Job page during individual simulations will not be visible within the Metrics Dashboard.

### Data View

This view presents the complete data for the selected object type in a tabular format. Users can easily navigate to specific objects by clicking on the rows. Additionally, they can apply filters or sort rows based on any specified column.

The data view is a comprehensive place to access all information across the entire platform - and is the base for nearly all other types of monitoring - be it creating Custom Views or creating automated Alerts.

### Automated Alerts

Alerts are defined as a set of rules that are designed to identify specific items or events that require immediate attention or further action. These rules are created based on predefined criteria, enabling the system to detect critical situations, anomalies, or deviations from expected behaviour. When the conditions specified in the alert rules are met, the system triggers events such as notifications, emails, etc., ensuring that appropriate actions can be taken promptly to address the identified issues.

### Creating Alerts

On the platform, users have the flexibility to create custom alerts tailored to their specific needs. Custom alerts encompass essential properties, including name, description, conditions, severity, and associated actions.

- Click on **Settings** icon and select **Alerts** in the dropdown menu option. Now you can view a list of alerts configured for the dashboard.
- Click on **Create**.
- Define the **Alert Name** by editing the New Alert header.
- **Severity**: Each custom alert can be assigned a severity level, such as _High_, _Medium_, or _Low_. This categorization allows users to prioritize alerts based on their importance and urgency. Different severity levels help stakeholders focus on critical issues
- **Table Name**: Select the table name from the dropdown menu.
- **Activate**: Click the activate checkbox to mark the alert as active. Activated alerts are evaluated, and the corresponding data is displayed as columns in the Monitoring Dashboard. Muted alerts are temporarily disabled and not evaluated, meaning they won't appear as columns in the dashboard during that period.
- Fill in the description for the new **Custom Alert**.

- **Actions**
  Choose an action type from the "Type" dropdown menu to determine the action that will be executed when the alert is triggered. The following actions can be associated with custom alerts:

  - **Send Notification**: The system can send notifications to selected users, or user roles informing them about the triggered alert.
  - **Add Alert Flag**: When an alert condition is met, users have the option to add a predefined flag to the object responsible for the alert. Flags serve as visual indicators to highlight objects that require attention.
  - **Create Review**: For Approved objects, users can choose to add an ongoing review to the object's responsibility and assign reviewers. This action facilitates a thorough review process for objects flagged by the custom alert.
  - **Send Email**: Users can configure the system to send email notifications to external users when an alert is triggered. The custom field associated with the objects should contain a string of comma-separated email addresses for users who should receive these emails.

!!! note

    Multiple actions can be triggered based on an alert.

- **Conditions**: Define the conditions that need to be met for an alert to be generated. These conditions are specified using rules based on the columns available in the Monitoring Dashboard Data. By utilizing data from the dashboard, users can set up criteria that trigger the alert when specific thresholds or patterns are detected.

- Click on **Create** to register the alert. A pop-up toast message will be displayed with the text reading Alert Created Successfully.
