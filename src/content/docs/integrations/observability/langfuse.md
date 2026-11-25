---
title: "Langfuse"
description: "Use Langfuse observations as an annotation queue ingestion source in GGX, so production traces can be reviewed by people."
---

[Langfuse](https://langfuse.com/docs) is an open-source platform for LLM observability, prompt management, and evaluations. GGX can fetch its observations into an annotation queue for human review.

## What it does in GGX

- Langfuse is an **Ingestion Source** for an annotation queue. GGX fetches observations from the Langfuse API for a date range you choose.
- Reviewers label them in the queue. Accepted interactions can become ground truth, and failures can become bugs or findings.

## How to connect

1. Open a project's annotation queue and go to its settings.
2. Set **Ingestion Source** to **Langfuse**.
3. Enter the **Langfuse Host URL** (it starts as `https://cloud.langfuse.com`), the **Langfuse Public Key**, and the **Langfuse Secret Key**.
4. Adjust the fetch script if you need to filter observations or rename columns. It is plain Python.

## Notes

- Langfuse has no organization-level integration entry in GGX. The keys belong to the queue.
- A fetch needs at least one observation in the selected date range.
