---
title: "Arize Phoenix"
description: "Bring Arize Phoenix traces into GGX annotation queues with a custom ingestion source, as GGX has no built-in Phoenix connection."
---

[Arize Phoenix](https://arize.com/docs/phoenix) is an AI observability and evaluation platform with OpenTelemetry-based tracing, evaluations, datasets, experiments, and human annotations.

## What GGX supports

GGX has no built-in Arize Phoenix connection. Arize Phoenix does not appear under **Org Settings → Integrations**, and it is not one of the built-in **Ingestion Sources** of an annotation queue (those are **Datasets**, **Datadog**, **Langfuse**, **Amazon S3**, and **Custom**).

## How to bring Arize Phoenix data into GGX

- **Custom ingestion source.** Set an annotation queue's **Ingestion Source** to **Custom** and write a Python fetch script that reads from the Arize Phoenix API and returns the records as a table. **Custom** is meant for sources such as internal APIs, warehouses, and data lakes.
- **Registered dataset.** Export the records, load them into a table, register it as a dataset, and use the **Datasets** ingestion source.

Keep the credentials for the API in environment variables or integration settings, not in the script.

See [Observability](../) for the review loop that follows, and [Annotation queues](../../../deploy-and-monitor/annotation-queues/) for queue setup.
