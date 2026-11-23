---
title: "Ingesting Data into Annotation Queues"
description: "Pull production data into a GGX annotation queue from datasets, Datadog, Langfuse, Amazon S3 or custom code, with sampling, preprocessing and scheduled fetches."
---

An annotation queue can fetch its own data instead of waiting for someone to upload files. You choose a source, write or adjust a short fetch script, and GGX runs it for a date range, on demand or on a schedule.

The running example on this page is a support agent in production: a queue fetches the last week of its chats from Langfuse, keeps a 10% sample, and adds them for review every week.

## Connect a data source

Open the queue, click **Edit** on the **Details** tab and turn on **Data Lake Connection**. Under **Data Fetching Logic**, pick an **Ingestion Source**. GGX fills in a starter script for it.

| Source | Fetches | Settings to fill in |
| --- | --- | --- |
| **Datasets** | Registered platform tables | **Input Tables**: the tables the script reads |
| **Datadog** | Spans from Datadog LLM Observability | **Datadog API Key**, **Datadog Application Key** |
| **Langfuse** | Observations from Langfuse | **Langfuse Host URL** (for example `https://cloud.langfuse.com`), **Langfuse Public Key**, **Langfuse Secret Key** |
| **Amazon S3** | Files stored in S3 | **S3 File Location** (for example `s3://my-bucket/data.parquet`), **AWS Access Key**, **AWS Secret Key** |
| **Custom** | Anything else, such as internal APIs or warehouses | None: write the whole script yourself |

For Datadog, Langfuse and Amazon S3, the starter script is hidden behind **Show Advanced Configuration**. Open it only if you need to change the query. Datasets and Custom show the script straight away.

Changing the source resets the source settings, so fill them in again.

### What the script receives

The script is the body of a Python function. It must `return` a table of records.

- `start_date` and `end_date` are the date range of the fetch.
- Each setting of the source is a variable, for example `langfuse_host`, `langfuse_public_key` and `langfuse_secret_key`.
- For **Datasets**, the selected tables are variables under their aliases.

The starter scripts filter by date and return the result. Add your own filters or column changes before the `return`.

## Fetch data

Save the queue, then click **Fetch Data** on the **Data Fetching Logic** panel. The button is disabled while you edit.

The **Fetch from Datalake** dialog asks for:

- **Name**: the name of this fetch.
- **Start Date** and **End Date**: the range passed to your script.
- **Schedule**: turn on to run later and repeat. Pick a **Scheduling Date** (a future date and time) and a **Recurrence**. The dialog lists the first iterations so you can check the dates.
- **Add data on completion**: tick to add the fetched records to the queue as soon as the fetch finishes.

With **Schedule** on, the name can use the placeholders `{start_date}`, `{end_date}`, `{current_iteration}` and `{current_date}`, so each run gets its own name.

Click **Run**.

### Recurrence options

The **Recurrence** list is built from the scheduling date: **Does not repeat**, **Hourly**, **Daily**, **Weekly on** the day of the scheduling date, **Monthly** (on the Nth weekday, on the last weekday, or on the date), **Quarterly** on the Nth or last weekday, and **Annually** on the date.

### Follow a fetch

The **Files & Ingestion** card on the **Details** tab shows how many files are in the queue, the data source, and the fetch status. Click **Manage Data Files** to open **Pending Data Files**. A completed fetch that was not set to add its data on completion shows **Add Data to Queue**. If a fetch had errors, click **Logs** to open its parameters (start and end date, schedule, recurrence, add on completion) and its job logs.

## Sampling

Production traffic is often too large to review in full. Turn on **Sampling** under the source to keep a share of each fetch before the data is saved.

- **Sampling Percentage**: from 1 to 100.
- **Sampling Type**: **Random** keeps a random share of all records. **Stratified** keeps the share within each group, so small groups stay represented.
- **Stratify Columns**: for **Stratified** only, the columns that define the groups, for example `topic` or `risk_tier`. At least one is required.

Sampling is applied to the result of your script, so it works the same for every source. A **Stratified** sample keeps the same percentage of each group.

## Preprocessing

Turn on **Preprocessing Logic** to change a data file before its records are appended to the queue. The code is the body of a function that receives the file as `data`, a pandas DataFrame with every column read as text, and returns the DataFrame to add. Use it to rename columns, drop test traffic or reshape chat messages. Preprocessing applies to every file added to the queue, uploaded or fetched.

## Data lake logic and preprocessing together

The order is: your fetch script runs, sampling reduces the result, the result is saved as a data file, and preprocessing runs when that file is added to the queue. Records that exactly duplicate records already in the queue are not added twice.

:::note
When **Enable Automated Judging** is on, the judge reviews new records as they are added. If the judge configuration is wrong, the records are still added, without judge results, and GGX reports the error. Correct the configuration and click **Rerun Judge**. See [Automated judging](../annotation-queues/#automated-judging).
:::

Next: [map the columns and choose reviewers](../annotation-queues/#setting-up-a-queue).
