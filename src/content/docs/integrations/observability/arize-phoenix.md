---
title: "Arize Phoenix"
description: "Connect Arize Phoenix traces, evaluations, datasets, and human annotations to GGX for governed monitoring, review, bug categorization, and AI lifecycle improvement."
---

[Arize Phoenix](https://arize.com/docs/phoenix) is an AI observability and evaluation platform with tracing, evaluations, prompt engineering, datasets, experiments, and human annotations. Phoenix supports OpenTelemetry-based tracing and can capture model calls, retrieval, tool use, and custom logic.

## How Phoenix fits with GGX

Phoenix helps teams debug and improve AI applications with traces, evaluators, datasets, and experiments. GGX can use Phoenix trace data as production monitoring input and connect it to review, approval, and lifecycle governance.

Use this pattern when:

- Your application is already instrumented with Phoenix or OpenInference.
- You want Phoenix traces and spans to become GGX monitoring cases.
- You want evaluator scores and human annotations to feed GGX ground truth.
- You want recurring Phoenix failure patterns to become categorized GGX bugs or findings.

## Trace-to-review workflow

1. Send Phoenix traces, spans, evaluator scores, dataset references, and human labels into GGX.
2. Use GGX rules and LLM judges to filter the trace volume into a smaller review queue.
3. Ask business SMEs or risk reviewers to confirm whether selected interactions are acceptable.
4. Add positive reviews to ground truth for future simulations and judge calibration.
5. Add negative reviews to GGX bugs or findings with failure categories and linked trace context.
6. Use those categories to track recurring issues and prove that fixes reduce failure frequency.

## GGX value add

Phoenix can show what happened inside an AI run and help teams evaluate it. GGX turns that evaluation signal into an operating process: reviewed traces become reusable ground truth, failures become managed remediation work, and monitoring becomes part of the same lifecycle used for refinement, approvals, deployment, and oversight.
