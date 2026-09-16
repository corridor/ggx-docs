# LangSmith
Source: https://docs.genguardx.ai/integrations/observability/langsmith/
Markdown: https://docs.genguardx.ai/integrations/observability/langsmith/index.md
Description: Use LangSmith traces with GGX to run judges, human reviews, ground truth promotion, bug tracking, and closed-loop AI monitoring.
[LangSmith](https://docs.smith.langchain.com/) provides observability for LLM applications, including traces, production metrics, dashboards, alerts, automations, online evaluations, annotation, and user feedback.

## How LangSmith fits with GGX

LangSmith is often the first place engineering teams inspect detailed traces for LangChain or other LLM applications. GGX can consume those traces as monitoring evidence and add lifecycle governance around them.

Use this pattern when:

- Engineering teams already instrument production applications with LangSmith.
- You want business, risk, or compliance reviewers to evaluate selected traces in GGX.
- You want positive production examples to become ground truth.
- You want negative examples to become categorized bugs or findings.
- You want LangSmith monitoring to feed future GGX judges, simulations, and approval evidence.

## Trace-to-review workflow

1. Export or stream LangSmith traces into GGX with prompt, response, model, metadata, evaluator scores, user feedback, and trace links.
2. Use GGX monitoring rules and judges to prioritize which traces need review.
3. Route selected traces to GGX human review or annotation queues.
4. Promote accepted traces to ground truth.
5. Convert rejected traces into bugs or findings, then categorize recurring failure patterns.
6. Use reviewed examples to improve GGX judges, reports, and regression test datasets.

## GGX value add

LangSmith helps teams observe and debug LLM behavior. GGX closes the lifecycle loop: monitoring evidence becomes ground truth, bugs, judge calibration data, approval evidence, and deployment guidance.

That makes production monitoring useful for the way teams manage AI systems, not just the way they inspect metrics.