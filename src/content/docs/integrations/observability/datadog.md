---
title: "Datadog"
description: "Use Datadog LLM Observability spans as an annotation queue ingestion source in GGX, so production traces can be reviewed by people."
---

[Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/) monitors LLM applications alongside infrastructure, APM, and logs. GGX can fetch its spans into an annotation queue, so product, risk, or compliance reviewers can judge them.

## What it does in GGX

- Datadog is an **Ingestion Source** for an annotation queue. GGX fetches LLM Observability spans for a date range you choose.
- Reviewers label the spans in the queue. Accepted interactions can become ground truth, and failures can become bugs or findings.

## How to connect

1. Open a project's annotation queue and go to its settings.
2. Set **Ingestion Source** to **Datadog**.
3. Enter the **Datadog API Key** and **Datadog Application Key**. Create them in Datadog under Organization Settings, API Keys and Application Keys. The application key needs the `apm_read` permission to query spans.
4. Adjust the fetch script if you need to filter spans or rename columns. It is plain Python.

## Notes

- Datadog has no organization-level integration entry in GGX. The keys belong to the queue.
- The default fetch script queries `api.datadoghq.com`. If your Datadog account is in another site, change the base URL in the script.
