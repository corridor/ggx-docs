---
title: "Annotation Queues"
description: "Use GGX Annotation Queues to bring human review into production monitoring, label live data, build ground truth, and turn feedback into auditable metrics."
---

It is important to add a Human element when monitoring activity in Production as not all trends can be caught in an automated way. New trends are not always caught using programmatic approaches, but programmatic approaches are useful for repetitive tasks. Bringing a balance of both evaluation methods is key to maintaining a good healthy production system.

The Annotation Queue capability is designed to bring in the human evaluation and labelling of production data - but also do it in an efficient way to reduce human error. This capability allows the validation of model outputs in real time by having annotators assess and label the production outcome. The capability can help track a variety of metrics, both standard and custom, on raw and annotated production data, organized digitally for the stakeholders.

The capability significantly improves the usual approach to annotating production data using Excel and Google Sheets, creating a more transparent and auditable system to monitor live performance.

![Annotation Queue Concept](./annotation-queue-concept.excalidraw.svg)

## Where annotation queues live

Annotation queues are listed under **Monitor & Track → Annotation Queues**, grouped by folder (for example production and staging traffic), with their status. Filter them by **Annotation Objective** or status, and click **Create** to add one.

![Monitor & Track → Annotation Queues: queues for production and staging traces, grouped by folder](./annotation-queues-list.jpg)

## Setting up a queue

A queue's **Details** tab configures what annotators see and record. Click **Edit** to change it.

- **Name** and **Description**: what the queue reviews and who reviews it.
- **Data Lake Connection**: fetch production data into the queue on demand or on a schedule. See [Ingesting Data](../annotation-queue-ingestion/).
- **Annotation Rubric**: the annotation objective and the feedback columns, described below.
- **Map columns**: the **ID Column**, the **Date Column** and the **Labeling Columns** shown to annotators.
- **Chat transcript**: for the **Entire Chat** and **Every Turn** objectives, the **Message Column** that holds the conversation in OpenAI messages format (a list of `role` and `content` pairs), and optionally the **Persona Name Column** and **Persona Description Column**, so chats are displayed as transcripts. For **Entire Chat**, a **Summary Column** can show a summary of each chat.
- **Chat Configuration**: closing questions asked when an annotator finishes reviewing a chat.
- **Enable assignees**, **Dedicated Reviewers** and **Send to other queues**: the review workflow, described below.

![Details tab of an annotation queue, scrolled to Map Columns and Chat Transcript: the ID, Date and Labeling columns, the message column, and the Chat Configuration box](./annotation-queue-columns.jpg)

### Annotation objective and feedback columns

The **Annotation Rubric** sets how annotators rate your data.

![Details tab of an annotation queue: the Annotation Rubric with the Entire Chat, Every Turn and Every Record objectives, and the Is Accurate and Judge Verdict feedback columns](./annotation-queue-rubric.jpg)

| Annotation objective | What one annotation covers | Type of the **Is Accurate** column |
| --- | --- | --- |
| **Entire Chat** | The conversation as a whole. One rating is applied to the complete chat. | **Chat Level**: one tick or cross for the whole conversation |
| **Every Turn** | Each response of the agent, which gets its own annotation. | **Message Level**: a like or dislike for each message or turn |
| **Every Record** | Each row of the data, treated as a separate annotation. | **Binary Assessment**: correct or incorrect for each row |

Every queue has an **Is Accurate** feedback column. It is marked **System Column**: you cannot rename or delete it, and its type changes with the objective you pick. Each rating shows as marked accurate, unmarked, or marked inaccurate, and the **Insights** tab counts them as correct, incorrect and unknown.

Add your own feedback fields with **Add New Column** and type a name for each. The feedback types are:

| Type | What the annotator provides | Objectives |
| --- | --- | --- |
| **Message Level** | A like or dislike for each message or turn in the chat | **Entire Chat**, **Every Turn** |
| **Chat Level** | One answer on whether the entire conversation had an issue | **Entire Chat**, **Every Turn** |
| **Binary Assessment** | Correct or incorrect for each record | **Every Record** |
| **Likert Scale** | A rating from 1 to 5 for each record | **Every Record** |
| **Free Text / Comment** | An open-ended note | All objectives |

The chat configuration applies only to the chat objectives. Switching a queue to **Every Record** clears it.

### Reviewers and routing

Turn on **Enable assignees** to add an **Assignee** column that annotators can edit in the **Labeling** tab and see in **Data**. Pick the people who can be assigned in **Dedicated Reviewers**. A reviewer who opens a queue that has reviewers lands on the records assigned to them; switch between **All Records** and **Assigned to Me** at the top of the **Labeling** tab. Everyone else sees all records.

To let reviewers hand records to another queue, map the **ID Column** and choose queues in **Send to other queues**. Only queues of the project that have an ID column mapped are listed. In the **Labeling** tab, the assignee editor then offers two modes: **Assign in this queue** and **Send to another queue**.

## Working in a queue

A queue has these tabs:

- **Data**: view or export the raw data.
- **Labeling**: the records to annotate, with their labeling columns, a **View Transcript** button for chats, the feedback summary, review status and judge verdict. Use the date range at the top to focus on a period, and **Create test dataset** to turn reviewed records into a dataset for evaluations.
- **Insights**: progress (total, pending, annotated and accuracy on rated records), counts over time, **Issues Found**, and reports. See [Finding Issues](../annotation-queue-issues/) and [Reports and Figures](../annotation-queue-reports/).
- **Judge**: an LLM judge that pre-labels records so annotators can focus where it matters.
- **Maintenance**: hidden until you open it from the **⋮** menu with **Open Maintenance**.

The **⋮** menu also offers **Export Queue Data**, **Move to Another Project** and **Archive**.

![Labeling tab: production chats with their condition, risk tier and topic, a transcript button, the review status and the judge verdict](./annotation-queue-labeling.jpg)

![Insights tab: overall progress of the queue and the number of correct, incorrect and unknown records by date](./annotation-queue-insights.jpg)

### Row actions

Right-click a row in **Data** or **Labeling** for **Open In New Tab** and **Copy Link**, which point at that record. The same menu has **Add to issue** (see [Finding Issues](../annotation-queue-issues/)) and, for queues with a **Message Column** mapped, **Add to dataset**. Right-click a column header for **Hide Column** and **Wrap Columns**.

### Adding chats to a dataset

Use **Add to dataset** to copy the chats of records into a Chat dataset for evaluations. Choose **A dataset that exists**, or **A new dataset** to create one. Chats the dataset already holds are skipped.

**Create test dataset** does the same for many records at once. It needs the **ID Column** and **Message Column** mapped. Click it, select the records, then fill the **Save test dataset** dialog: pick the **Chat dataset**, optionally add **Additional columns** (the ID and message columns are always included), and click **Append records**.

### Maintenance

The **Maintenance** tab runs a script on the queue data. It offers starter snippets: **Rename column**, **Remove duplicate rows** and **Remove empty columns**. The queue data is in the variable `queue_data`, a DuckDB DataFrame; change `queue_data` to change the queue. Click **Preview Data** to check the result, then **Update Queue Data!** to apply it. The update cannot be reverted and is not audited.

### Automated judging

On the **Judge** tab, turn on **Enable Automated Judging** and write the **Instructions for the Judge**. The instructions can reference columns of the data, such as `{Topic}` or `{messages}`, and define the verdicts the judge returns. Click **Rerun Judge** to judge the records again after changing the instructions. Judge verdicts appear in the Labeling tab next to the human review, so you can see where the judge and the reviewers disagree.

![Judge tab: automated judging enabled, with instructions that reference the topic, risk tier and chat, and the list of possible verdicts](./annotation-queue-judge.jpg)

## Inviting annotators

All users with access to the project's annotation queues can collaborate on labeling. The platform records every label change and lets annotators leave notes.

## Benefits of Annotation Queues:

- **Easy onboarding** of data annotated in an external environment.
- Easy to follow and **intuitive user-interface** to annotate data.
- **Auditable annotations**, platform records all modifications to the data and labels.
- **Automatic ingestion** of production data, from datasets, Datadog, Langfuse, Amazon S3 or your own code, with optional sampling.
- **Enhanced Collaboration** with other reviewers.
- **Automated Performance and Progress** tracking.
- Smart algorithms to **expedite the labeling process**.

:::note[From labels to better evaluation]
Labelled and ground-truth data is the raw material for continuous improvement. Recurring failure categories surfaced during annotation can be codified into new judges and [reports](../../evaluate-and-approve/reporting/), which then run across all agents — turning human insight into automated checks over time. The same labelled data also serves as the ground truth for [validating those evaluators](../../evaluate-and-approve/simulation/#validating-an-evaluator).
:::
