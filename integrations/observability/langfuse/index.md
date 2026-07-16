# Langfuse
Source: https://docs.genguardx.ai/integrations/observability/langfuse/
Markdown: https://docs.genguardx.ai/integrations/observability/langfuse/index.md
Description: Use Langfuse traces, scores, datasets, and annotation queues with GGX to close the monitoring loop across judges, human review, ground truth, bugs, and approvals.
[Langfuse](https://langfuse.com/docs) is an open-source AI engineering platform for LLM observability, prompt management, evaluations, dashboards, datasets, experiments, user feedback, and annotation queues.

## How Langfuse fits with GGX

Langfuse can capture production traces and scores across LLM calls, retrieval, embedding, API calls, sessions, agents, and user interactions. GGX can connect those traces to governed monitoring and review workflows.

Use this pattern when:

- You already use Langfuse as the trace and evaluation layer for LLM applications.
- You want selected Langfuse traces to be reviewed by SMEs or risk teams in GGX.
- You want Langfuse scores and user feedback to influence GGX monitoring rules.
- You want reviewed Langfuse examples to power future GGX datasets, judges, and approval evidence.

## Trace-to-review workflow

1. Send Langfuse traces, scores, sessions, prompt versions, user feedback, and metadata to GGX.
2. Use GGX monitoring logic to identify traces that need judge review, human review, or no review.
3. Promote positively reviewed traces into ground truth.
4. Convert negatively reviewed traces into GGX bugs or findings.
5. Categorize common failures so teams can see where prompt, RAG, model, tool, or policy changes are needed.
6. Reuse those examples in GGX simulations and judge-development workflows.

## GGX value add

Langfuse provides strong observability and evaluation workflows. GGX makes the monitoring lifecycle actionable across stakeholders: positive monitoring reviews become test data, negative reviews become remediation work, and both feed the evaluation and approval system used to manage production AI.