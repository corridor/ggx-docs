---
title: "Deployment and Monitoring"
description: "Deploy approved GGX agent artifacts to production and monitor reliability, performance, accuracy, alerts, and human annotation queues for live GenAI systems."
---

Once an agent is registered on the GGX platform, it can be [evaluated and approved](../evaluate-and-approve/) within the system. After approval, the locked agent artifact can be [exported directly to production](direct-to-production/).

For an agent in production, **monitoring is essential** to maintaining the reliability, performance, and accuracy of systems in real-world scenarios. The platform **automates production monitoring** by ingesting data from relevant systems, generating performance metrics, providing intuitive monitoring dashboards and alerting capabilities. Additionally, it offers **Annotation Queues**, enabling human reviewers to evaluate and label production data, with automated dashboards for key insights and statistics.

For request-level visibility, [Tracing](../tracing/) records every model call, retrieval and tool step your agents, deployments and agents make, so you can search, score, evaluate and alert on live traffic.
