---
title: "Agent Observability"
description: "Agent observability in GGX: trace every LLM call, tool call, retrieval and autonomous agent decision, then mask, price, score, evaluate, monitor and keep it as evidence."
---

Agent observability shows what your agents did in production and why. GGX records each request your agents and deployments handle as a **trace** that covers every LLM call, tool call, retrieval and autonomous decision the agent made along the way. You can open a trace, mask it, price it, score it, evaluate it and keep it as evidence. These pages cover what is captured, how to send it, and how to work with it once it is in.

In the app, agent observability lives under **Monitor & Track → Tracing**.

## Traces, spans and sessions

These pages follow one example throughout: a _Card Replacement Assistant_, a chat agent that helps cardholders block a lost card and order a new one.

Everything GGX records sits at one of three levels, each nested inside the one above: a session holds traces, and a trace holds spans.

<figure class="ggx-figure ggx-figure--wide">

![A session is one conversation with a cardholder and holds three traces in order. Trace 2, "Block it and send a new one", is opened to show its tree of spans: a chain span for the assistant's turn that contains a retriever span, an LLM span and a tool span, each with its own timing.](./session-trace-span.svg)

<figcaption>One conversation with the Card Replacement Assistant: a session of three traces, with the second trace opened to show its spans.</figcaption>
</figure>

| Level | What it is | In the example |
| --- | --- | --- |
| **Session** | The whole conversation: every trace that shares a session id, in order. | One cardholder's chat, from "I lost my card" to "Thanks". |
| **Trace** | One request: a message and everything the assistant did to answer it. | "Block it and send a new one" and the work behind the reply. |
| **Span** | One step inside a request: an LLM call, a retrieval, a tool call, an agent deciding what to do next, or a chain that groups them. | The call to `gpt-4o-mini`, the _card policy_ lookup, the _block card_ tool. |

A span can contain other spans, which is how a trace becomes a tree: in the figure, the _card assistant turn_ chain contains the retrieval, the LLM call and the tool call. LLM calls carry tokens and cost; every span carries its timing and status.

## What gets captured

For every span GGX keeps:

- its name, kind, start and end, and status
- the model and provider, for model calls
- input and output, masked by your project's [data masking](data-masking/) policy
- token counts, including cached and reasoning tokens
- time to first token, where the instrumentation reports it
- errors
- [cost](cost-and-retention/)

Each trace also records which project, deployment and agent version it belongs to, so every run can be traced back to the approved asset that produced it.

## Where to go next

**Start here**

- [Sending traces](sending-traces/): the Python SDK, your own tools, agent frameworks and any OpenTelemetry exporter.
- [Data masking](data-masking/): what is hidden before anything is stored, and how to manage a project's policy.

**Use it**

- [Exploring traces](exploring-traces/): the trace list, a single trace, the span inspector, errors and data quality.
- [Search, analytics and export](search-and-analytics/): the query language, the Spans tab, metadata dimensions, charts, saved views and export.
- [Agents and sessions](agents-and-sessions/): the agent graph, trajectory flags, conversations and simulation jobs.
- [Scores and feedback](scores-and-feedback/): reviewer scores, score configs and end-user feedback from your application.
- [Evaluators](evaluators/): judges that record a verdict on live traffic.
- [Monitors](monitors/): thresholds on traffic, latency, cost and quality, with alerts.
- [Governance signals](governance-signals/): findings GGX files when it sees a risk in your traces.

**Operate it**

- [Cost and retention](cost-and-retention/): price sheets, retention, sampling and access.
- [API reference](api-reference/): the tracing endpoints.
