---
title: "Datadog"
description: "Connect Datadog LLM Observability traces and incidents to GGX for AI judges, human review, ground truth creation, bug categorization, and lifecycle governance."
---

[Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/) helps teams monitor LLM applications alongside infrastructure, APM, logs, security, dashboards, and alerting. It is useful when AI behavior needs to be understood together with production system health.

## How Datadog fits with GGX

Datadog is often the operational system of record for production health. GGX can connect Datadog LLM traces, alerts, incidents, or linked logs into AI-specific monitoring and review workflows.

Use this pattern when:

- Your SRE or platform team monitors AI applications in Datadog.
- LLM issues need to be reviewed by product, risk, compliance, or model owners.
- Datadog alerts should trigger GGX review queues or annotation workflows.
- Production traces should feed GGX ground truth, bugs, judges, and approval evidence.

## Trace-to-review workflow

1. Send Datadog LLM traces, alerts, incidents, logs, service metadata, latency, cost, model, prompt, response, and error context to GGX.
2. Use GGX judges and rules to separate normal telemetry from interactions that need human review.
3. Route the narrowed review set to the right SMEs, risk reviewers, or annotation queues.
4. Add accepted interactions to ground truth.
5. Add failed interactions to bugs or findings, grouped by recurring failure category.
6. Use the resulting evidence to improve prompts, retrieval, model routing, guardrails, and deployment readiness.

## GGX value add

Datadog tells teams when something happened in production. GGX helps teams decide what that event means for AI quality, risk, approvals, and future releases. The result is a feedback loop where monitoring improves the AI system rather than only reporting metrics about it.
