---
title: "Observability"
description: "Bring production traces into GGX annotation queues from Datadog or Langfuse, connect Weights & Biases and Fiddler AI, and move other tools' traces in with a custom source."
---

AI observability tools collect traces, latency, cost, and scores from production. GGX turns that signal into review: traces become annotation queue items, review outcomes become ground truth, and common failures become categorized bugs.

How a tool connects depends on the tool.

## How each tool connects

| Tool | How it connects to GGX |
| --- | --- |
| [Datadog LLM Observability](datadog/) | A built-in **Ingestion Source** of an annotation queue. GGX fetches LLM Observability spans with your Datadog API and application keys. |
| [Langfuse](langfuse/) | A built-in **Ingestion Source** of an annotation queue. GGX fetches observations with your Langfuse host and keys. |
| [Weights & Biases](weights-and-biases/) | An organization integration under **Observability**. Add an API key and, for a dedicated deployment, a base URL. |
| [Fiddler AI](fiddler-ai/) | An organization integration under **Observability**. Add an API key and your Fiddler URL. |
| [LangSmith](langsmith/) | No built-in connection. Bring traces in with the **Custom** ingestion source or a registered dataset. |
| [Arize Phoenix](arize-phoenix/) | No built-in connection. Bring traces in with the **Custom** ingestion source or a registered dataset. |
| [Humanloop](humanloop/) | No built-in connection. Humanloop is sunset: only historical exports apply. |

## Bring traces into an annotation queue

An annotation queue pulls its data from an **Ingestion Source**, which you choose in the queue's settings: **Datasets**, **Datadog**, **Langfuse**, **Amazon S3**, or **Custom**. **Custom** fetches data from sources such as internal APIs, warehouses, and data lakes with a Python fetch script. See [Annotation queues](../../deploy-and-monitor/annotation-queues/).

Once the data is in a queue, GGX supports the review loop:

1. **Reduce the review funnel.** Use heuristics, automated checks, and LLM judges to find the traces that need human attention.
2. **Run human reviews.** Route selected traces to business experts, risk teams, or model owners.
3. **Promote positive reviews.** Add acceptable traces to ground truth so future tests and monitoring are more representative.
4. **Capture negative reviews.** Record a bug or finding with the relevant prompt, model, context, and reviewer notes.
5. **Improve judges.** Use reviewed traces and failure categories to build and calibrate LLM-as-a-judge reports.

## What to bring in

Bring enough context for review and fixes:

- Prompt, response, model, and provider.
- Retrieval context, tool calls, agent steps, and error details.
- User feedback, ratings, and session metadata.
- Existing scores from your observability tool, such as toxicity, hallucination, latency, or cost.
- Business context such as product area, channel, or application version.

## Related pages

- [Datadog](datadog/)
- [Langfuse](langfuse/)
- [Weights & Biases](weights-and-biases/)
- [Fiddler AI](fiddler-ai/)
- [LangSmith](langsmith/)
- [Arize Phoenix](arize-phoenix/)
- [Humanloop](humanloop/)
