---
title: "Humanloop"
description: "Humanloop is sunset and has no built-in GGX connection; load historical exports through a registered dataset or custom ingestion source."
---

[Humanloop](https://humanloop.com/docs) provided LLM evaluation, prompt management, logs, and human feedback. Its documentation notes that the platform was sunset on September 8, 2025, so use this only for data you already exported.

## What GGX supports

GGX has no built-in Humanloop connection. Humanloop does not appear under **Org Settings → Integrations**, and it is not one of the built-in **Ingestion Sources** of an annotation queue (those are **Datasets**, **Datadog**, **Langfuse**, **Amazon S3**, and **Custom**).

## How to bring Humanloop data into GGX

- **Custom ingestion source.** Set an annotation queue's **Ingestion Source** to **Custom** and write a Python fetch script that reads from the Humanloop API and returns the records as a table. **Custom** is meant for sources such as internal APIs, warehouses, and data lakes.
- **Registered dataset.** Export the records, load them into a table, register it as a dataset, and use the **Datasets** ingestion source.

Keep the credentials for the API in environment variables or integration settings, not in the script.

See [Observability](../) for the review loop that follows, and [Annotation queues](../../../deploy-and-monitor/annotation-queues/) for queue setup.
