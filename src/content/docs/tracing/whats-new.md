---
title: "What's New in Tracing"
description: "Release notes for GGX tracing and observability: agent frameworks, simulation job traces, search and analytics, monitors, governance signals, evaluators and data masking."
---

Changes to the tracing features, newest first.

## 5 Oct 2026

- **Simulation jobs and multi-agent runs.** A [simulation job](../agents-and-sessions/#simulation-jobs) now traces every record, shows what it spent in its header and on **Job Results**, and links each result row to its trace. In a LangGraph run each agent's model calls and tools sit under that agent, agent runs are counted, a call repeated by two different agents is no longer flagged, and tool and model time no longer double-count parallel work. Mark a hand-written agent with `@tracing.agent`.

## 25 Sep 2026

- **Clearer graph and messages.** The [agent graph](../agents-and-sessions/#the-agent-graph) reads top to bottom and colors each step by kind; a model reply that only calls a tool shows the call, and chats wrapped as `{"messages": [...]}` read as conversations.
- **Every attribute in one place.** A step's [Attributes tab](../exploring-traces/#the-span-inspector) now shows everything recorded for it as one searchable document, with its scores and evaluations, a note of which of your attributes each value came from, and **Copy as JSON**. **Show only unmapped** brings back the previous view.

## 24 Sep 2026

- **Agent frameworks.** LangChain and LangGraph pipelines running in GGX are traced node by node, with each node on the agent graph. For your own applications, new [SDK extras](../sending-traces/#frameworks) cover LangGraph, LlamaIndex, CrewAI and the OpenAI Agents SDK, and `tracing.init()` turns on everything installed. A model call seen by both a framework and a model library is counted and priced once.
- **Easier to find your way.** Tabs grouped into Explore, Quality and Alerts; readable questions and answers in the trace list with status, latency and cost up front; sessions shown as conversations; clearer charts when there is little data; and empty pages that explain what to do first.
- **Tool spans.** Mark your own tool functions with [`@tracing.tool`](../sending-traces/#your-own-tools) (or `tracing.trace_tool`) to see each tool call, with its arguments and result, in the trace.
- **Side panel.** Traces now open in a side panel over the list, with arrows to step through the list and a link to the full page.
- **Search and analytics.** A [query language](../search-and-analytics/) on Traces and Spans, a Spans tab that searches every step, metadata dimensions, an Analytics tab, saved views, a column picker and audited CSV and JSON Lines export.
- **Monitors and governance signals.** [Monitors](../monitors/) with alerts in GGX, by email and to Slack, and [governance signals](../governance-signals/): findings from eight investigators, linked to the assets they concern, with a status workflow and risk-assessment hand-off.
- **Exact version links.** Pipeline and asset links on a trace now open the exact version the trace ran.
- **Agent views.** An agent graph on every trace, [flags](../agents-and-sessions/#trajectory-flags) for repeated tool calls, repeated calls in a row, cost outliers and empty answers, and first and last messages, agent work and flags on sessions.
- **Evaluator spending safeguards.** A daily cap, backoff, automatic switch-off and paused backfills.
- **Evaluators.** Six judge templates, custom rubrics, continuous judging of live traffic, backfill, evaluation trends, and on-demand judging of a trace, span or session. See [Evaluators](../evaluators/).
- **Data masking.** [Masking](../data-masking/) of personal data before storage, per-project content capture, custom rules, and a stamp on every span proving which policy masked it.
- **Errors and data quality.** Error details and events on failed steps, time to first token, data-quality flags, and 50th, 90th and 99th percentile latency.
- **Sticky time range.** Your chosen time range now stays in place as you move between tracing pages.
- **Scores and feedback.** [Scores](../scores-and-feedback/) on traces and spans, score configs, end-user feedback from the SDK and from deployments, and score columns and filters in the trace list.
- **Unpriced models.** The unpriced-models banner now covers the whole range you are viewing, and calls with unknown prices are no longer counted as free.
- **Platform trace filters.** The **Both** and **Platform only** trace filters now take effect.
