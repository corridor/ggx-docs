# Observability
Source: https://docs.genguardx.ai/integrations/observability/
Markdown: https://docs.genguardx.ai/integrations/observability/index.md
Description: Connect AI observability traces from LangSmith, Arize Phoenix, Langfuse, Humanloop, Datadog, and other tools to GGX for judges, human review, ground truth, bug categorization, and closed-loop AI lifecycle governance.
AI observability tools help teams collect traces, inspect runs, measure latency and cost, evaluate outputs, and understand production behavior. GGX can sit alongside these tools by connecting their traces into the GGX monitoring and review workflow.

The benefit is not just another dashboard. GGX helps make the AI lifecycle seamless: production traces become review queues, review outcomes become ground truth, common failures become categorized bugs, and the same evidence feeds future judges, evaluations, approvals, and deployment decisions.

## Supported observability patterns

| Tool | Typical use | GGX connection pattern |
| --- | --- | --- |
| [LangSmith](langsmith/) | Trace, debug, evaluate, and monitor LangChain and broader LLM applications. | Export or stream traces into GGX monitoring, then run judges and human reviews on selected interactions. |
| [Arize Phoenix](arize-phoenix/) | OpenTelemetry-based AI tracing, evaluations, prompt iteration, datasets, and experiments. | Bring traces, spans, evaluator outputs, and human labels into GGX as monitoring evidence and reusable test cases. |
| [Langfuse](langfuse/) | Open-source LLM observability, prompt management, evaluations, dashboards, and annotation queues. | Connect traces and scores to GGX so monitoring outcomes can become ground truth, bugs, and approval evidence. |
| [Humanloop](humanloop/) | Evaluation, prompt management, observability, human feedback, and production log review. | Import logs and review outcomes into GGX for governed SME review, judge creation, and lifecycle evidence. |
| [Datadog LLM Observability](datadog/) | Monitor LLM applications alongside broader infrastructure, APM, logs, and security telemetry. | Connect LLM traces or incidents to GGX so AI-specific quality review feeds testing, approvals, and remediation workflows. |

## What GGX adds

Observability platforms can show what happened. GGX turns that signal into governed lifecycle action.

1. **Connect traces:** Import production traces, spans, prompts, responses, metadata, scores, and user feedback from the observability tool.
2. **Reduce the review funnel:** Use heuristics, automated checks, and LLM judges to identify which traces need human attention.
3. **Run human reviews:** Route selected traces to business SMEs, risk teams, model owners, or annotation queues.
4. **Promote positive reviews:** If a reviewed trace is acceptable, add it to ground truth so future tests and monitoring become more representative.
5. **Capture negative reviews:** If a reviewed trace fails, create a bug or finding with the relevant prompt, model, RAG context, trace metadata, and reviewer notes.
6. **Categorize common bugs:** Group repeated issues into failure categories such as hallucination, retrieval miss, bad refusal, toxicity, policy breach, tool error, latency, or user-intent mismatch.
7. **Improve judges:** Use reviewed traces and failure categories to build, calibrate, and validate LLM-as-a-judge reports.
8. **Close the loop:** Feed the resulting ground truth, bugs, judges, and reports back into refinement, approval, deployment, and ongoing monitoring.

This turns monitoring from a static set of metrics into a practical operating system for managing and improving AI applications.

## Choosing what to send to GGX

Send enough trace context for review and remediation:

- Prompt, response, model, model version, route, and provider.
- Retrieval context, citations, tool calls, agent steps, and error details.
- User feedback, thumbs up/down, ratings, comments, escalation flags, and session metadata.
- Existing observability scores such as toxicity, hallucination, latency, cost, groundedness, retrieval quality, or custom evaluator results.
- Business context such as product area, customer segment, channel, workflow, policy, or approved application version.

GGX can then combine this with its own registered assets, reports, approval workflows, and monitoring logic.

## Related pages

- [LangSmith](langsmith/)
- [Arize Phoenix](arize-phoenix/)
- [Langfuse](langfuse/)
- [Humanloop](humanloop/)
- [Datadog](datadog/)