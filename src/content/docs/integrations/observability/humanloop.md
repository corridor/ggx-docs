---
title: "Humanloop"
description: "Connect Humanloop logs, evaluations, prompt management, and human feedback workflows to GGX for closed-loop AI lifecycle governance."
---

[Humanloop](https://humanloop.com/docs) provides LLM evaluation, prompt management, observability, logs, human feedback, and reviewer workflows. Humanloop's documentation notes that the Humanloop platform will be sunset on September 8, 2025, so teams should confirm their current deployment and migration path before building new integrations.

## How Humanloop fits with GGX

Humanloop logs and evaluations can provide useful review and product-feedback signals. GGX can ingest those signals and connect them to governed monitoring, ground truth, bug tracking, judge creation, and approval evidence.

Use this pattern when:

- Historical Humanloop logs contain useful production examples.
- Humanloop human feedback or evaluator results should be preserved in GGX.
- Your team is migrating review workflows into GGX.
- You want production review outcomes to feed ongoing GGX monitoring and evaluation.

## Trace-to-review workflow

1. Export Humanloop logs, prompts, evaluation results, user feedback, reviewer labels, and metadata.
2. Import the records into GGX monitoring or datasets.
3. Run GGX judges to triage which records need human review.
4. Promote positive reviews to ground truth.
5. Convert negative reviews into bugs or findings with failure categories.
6. Use the resulting examples to create or improve GGX judges, reports, and simulations.

## GGX value add

Humanloop-style feedback loops are strongest when they affect future development and deployment decisions. GGX keeps that loop active: monitoring evidence becomes test data, judge calibration, bug categories, approval evidence, and deployment guidance in one lifecycle.
