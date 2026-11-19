---
title: "Deployment and Monitoring"
description: "Deploy approved GGX agent artifacts to production and monitor reliability, performance, accuracy, alerts, and human annotation queues for live GenAI systems."
---

Once an agent is registered on the GGX platform, it can be [evaluated and approved](../evaluate-and-approve/) within the system. After approval, the locked agent artifact can be [exported directly to production](direct-to-production/).

For an agent in production, **monitoring is essential** to maintaining the reliability, performance, and accuracy of systems in real-world scenarios. The platform **automates production monitoring** by ingesting data from relevant systems, generating performance metrics, providing intuitive monitoring dashboards and alerting capabilities. Additionally, it offers **Annotation Queues**, enabling human reviewers to evaluate and label production data, with automated dashboards for key insights and statistics.

For request-level visibility, [Agent Observability](../agent-observability/) traces every LLM call, tool call, retrieval and autonomous decision your agents and deployments make, so you can search, score, evaluate and alert on live traffic.


## What does deployment and monitoring cover?

| Capability | What it gives you |
| --- | --- |
| [Direct to production](direct-to-production/) | Export the approved artifact to production runtimes, APIs, containers or CI/CD |
| [Performance](performance/) | Recurring jobs, metrics dashboards, thresholds and alerts for approved objects |
| [Oversight](oversight/) | Governance dashboards, role-based views and automated alerts across registered objects |
| [Annotation queues](annotation-queues/) | Human reviewers label and evaluate production data |

## When should I use it?

Use this section once an agent has passed [evaluation and approval](../evaluate-and-approve/) and you need to ship it and keep watching it. For request-level debugging of live traffic, use [Agent Observability](../agent-observability/).
