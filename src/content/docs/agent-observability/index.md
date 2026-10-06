---
title: "Agent Observability"
description: "Agent observability in GGX: trace every LLM call, tool call, retrieval and autonomous agent decision, then mask, price, score, evaluate, monitor and keep it as evidence."
---

Agent observability shows what your agents did in production and why. GGX records each request your agents and deployments handle as a **trace** that covers every LLM call, tool call, retrieval and autonomous decision the agent made along the way. You can open a trace, mask it, price it, score it, evaluate it and keep it as evidence. These pages cover what is captured, how to send it, and how to work with it once it is in.

In the app, agent observability lives under **Monitor & Track → Tracing**.

## Traces, spans and sessions

These pages follow one example throughout: a _Card Replacement Assistant_, a chat agent that helps cardholders block a lost card and order a new one.

- A **trace** is one request: a cardholder's message and everything the assistant did to answer it.
- A **span** is one step inside that request: an LLM call, a document retrieval, a tool call such as _lookup card status_, an agent deciding what to do next, or a chain that groups them.
- A **session** is the whole conversation: every trace that shares a session id, in order.

```text
Session  chat with one cardholder
├── Trace 1  "I lost my card"
├── Trace 2  "Block it and send a new one"
│   └── chain      card assistant turn          3.1 s
│       ├── retriever  card policy
│       ├── llm        gpt-4o-mini              1,036 → 58 tokens
│       └── tool       block card               0.4 s
└── Trace 3  "Thanks"
```

A session groups traces, and a trace is a tree of spans. Model calls carry tokens and cost; every span carries its timing and status.

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
