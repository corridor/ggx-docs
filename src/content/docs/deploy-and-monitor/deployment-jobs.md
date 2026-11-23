---
title: "Deployment Jobs, Chats and Insights"
description: "Run a GGX deployment over a table of requests, schedule recurring runs with threshold alerts, review its chats, and chart its invocations with custom figures."
---

Beyond serving requests, a deployment can be tested and watched from inside GGX. This page uses one example: a deployment of a support agent that takes a customer question as its request.

## Run a job on a deployment

A deployment job sends each row of a table to the deployment as one request and records the response in the standard job results.

1. Open the deployment and click **Run**.
2. In the job form, choose the data. The table needs a `request` column; its type is the deployment's **Request Type**, or text when none is set.
3. Click **Run Job**.

Deployment jobs support single-turn runs only. Each job appears in the **Jobs** tab, and the **Dashboard** tab gives a quick view of a recently run job, the same as for other assets. See [Simulation](../../evaluate-and-approve/simulation/) for the job form.

The request goes through the deployment's endpoint logic. If the deployment has no **Request Type**, the `request` value is read as JSON. If it has no **Response Type**, the response must be JSON-compatible.

## Schedule a job

To keep checking a deployment, open the **Scheduling** panel of the job form:

- **Start Date** and **Time**: when the first run starts. Leave them empty to run immediately.
- **Recurrence**: **Does not repeat**, **Hourly**, **Daily**, **Weekly on** the weekday, **Monthly**, **Quarterly** or **Annually**. The list follows the start date. See [Running a task on a schedule](../performance/#running-a-task-on-a-schedule) for the full list.

When a run ends, GGX schedules the next one.

## Alerts

To be told when a run goes wrong, set a lower and an upper threshold for each metric under **Metric Thresholds**, then open the **Alerts** panel and choose people in **Notify**. When a run completes and any metric is outside its thresholds, each person gets one notification in GGX listing the metrics that breached, and an email if your administrator has configured an email provider. Recurring runs keep the same people.

## Chats

The **Chats** tab collects and reviews conversations with the deployment. It is the deployment's feedback portal, the same page as under [Feedback portals](../../evaluate-and-approve/feedback-portals/). A deployment has none until someone clicks **Add chat**, which creates the portal and links it to the deployment.

## Insights

The **Insights** tab holds custom figures drawn from the deployment's invocation data: traffic, reliability, latency, or anything you compute. Pick a date range at the top, then click **Add Custom Figure**:

- **Name**.
- **Width**: **50%** or **100%**.
- **Figure Logic**: Python code that returns a Plotly figure, a Markdown string or a pandas DataFrame, which is shown as a table. The invocation data is in the variable `data`, a DuckDB DataFrame. **View Examples** shows one of each.

Drag figures to reorder them. Only people with write access can add, edit or reorder figures.
