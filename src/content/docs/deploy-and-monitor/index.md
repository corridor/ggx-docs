---
title: "Deployment and Monitoring"
description: "Deploy approved GGX agent artifacts to production and monitor reliability, performance, accuracy, alerts, and human annotation queues for live GenAI systems."
---

Once an agent is registered on the GGX platform, it can be [evaluated and approved](../evaluate-and-approve/) within the system. After approval, the locked agent artifact can be [exported directly to production](direct-to-production/).

For an agent in production, **monitoring is essential** to maintaining the reliability, performance, and accuracy of systems in real-world scenarios. The platform **automates production monitoring** by ingesting data from relevant systems, generating performance metrics, providing intuitive monitoring dashboards and alerting capabilities. Additionally, it offers **Annotation Queues**, enabling human reviewers to evaluate and label production data, with automated dashboards for key insights and statistics.


## What does deployment and monitoring cover?

| Capability | Where | What it gives you |
| --- | --- | --- |
| [Deployments and direct to production](direct-to-production/) | Risk & Compliance → Deployments | Record where each approved agent runs and how it is called, and export locked artifacts to production |
| [Deployment jobs, chats and insights](deployment-jobs/) | Risk & Compliance → Deployments | Run and schedule jobs on a deployment, review its chats, and chart its invocations |
| [Request and response types, custom interfaces](deployment-request-types/) | Risk & Compliance → Deployments → Code | Set the types of a deployment and serve your own page from it |
| [Performance tracking](performance/) | Monitor & Track → Monitoring | Monitoring tasks that run on a schedule, chart production metrics against thresholds, and alert chosen people |
| [Governance oversight](oversight/) | Project Home | The lifecycle and evidence of a whole project at a glance |
| [Annotation queues](annotation-queues/) | Monitor & Track → Annotation Queues | Human reviewers, helped by an LLM judge, label production data |
| [Ingesting data](annotation-queue-ingestion/) | Annotation Queues → Details | Fetch production data from datasets, Datadog, Langfuse, S3 or custom code, with sampling |
| [Finding issues](annotation-queue-issues/) | Annotation Queues → Insights | Corra and reviewers find recurring problems and triage them with evidence |
| [Reports and figures](annotation-queue-reports/) | Annotation Queues → Insights | Custom charts and tables, live or as snapshots |

## When should I use it?

Use this section once an agent has passed [evaluation and approval](../evaluate-and-approve/) and you need to ship it and keep watching it.
