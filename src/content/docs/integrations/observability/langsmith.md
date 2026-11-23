---
title: "LangSmith"
description: "Bring LangSmith traces into GGX annotation queues with a custom ingestion source, as GGX has no built-in LangSmith connection."
---

[LangSmith](https://docs.smith.langchain.com/) provides traces, production metrics, online evaluations, annotation, and user feedback for LLM applications.

## What GGX supports

GGX has no built-in LangSmith connection. LangSmith does not appear under **Org Settings → Integrations**, and it is not one of the built-in **Ingestion Sources** of an annotation queue (those are **Datasets**, **Datadog**, **Langfuse**, **Amazon S3**, and **Custom**).

## How to bring LangSmith data into GGX

- **Custom ingestion source.** Set an annotation queue's **Ingestion Source** to **Custom** and write a Python fetch script that reads from the LangSmith API and returns the records as a table. **Custom** is meant for sources such as internal APIs, warehouses, and data lakes.
- **Registered dataset.** Export the records, load them into a table, register it as a dataset, and use the **Datasets** ingestion source.

Keep the credentials for the API in environment variables or integration settings, not in the script.

See [Observability](../) for the review loop that follows, and [Annotation queues](../../../deploy-and-monitor/annotation-queues/) for queue setup.
