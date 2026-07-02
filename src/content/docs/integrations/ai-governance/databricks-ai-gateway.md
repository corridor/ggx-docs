---
title: "Databricks AI Gateway"
description: "Compare Databricks Unity AI Gateway with GGX for GenAI governance, automated compliance testing, approval evidence, production monitoring, and risk management."
---

Databricks Unity AI Gateway and GGX solve adjacent governance problems.

Databricks focuses on governing AI service access and runtime traffic inside the Databricks ecosystem. GGX focuses on the end-to-end Responsible AI lifecycle: registering GenAI assets, testing risk and business performance, producing approval evidence, monitoring production behavior, and feeding findings back into refinement.

## Executive summary

Databricks AI Gateway is the **runtime AI service control plane** for Databricks-centered deployments. It answers:

- Who can call this AI service?
- Which model or MCP service does traffic reach?
- How much usage or cost is allowed?
- Which request or response policies should be enforced?
- What happened at the request, token, latency, cost, and payload level?

GGX provides the **Responsible AI lifecycle management**. It answers:

- What stage of the lifecycle is the GenAI use case, agent, etc. at - Planning, Development, Deployed?
- Which risks matter for this use case?
- What automated and manual tests prove readiness?
- Who reviewed the evidence and approved production release?
- What were the issues that were reported - and what changed between versions to resolve them?
- What is happening in production, and which failures require human review?
- How does production feedback become new evaluation data?

## Databricks AI Gateway value prop

Databricks describes Unity AI Gateway as its governance solution for enterprise AI, built on Unity Catalog. Its core value is controlling and observing AI service interactions in Databricks:

- **Access governance:** Register models, agents, MCP services, functions, and HTTP connections as Unity Catalog securable objects, then grant or revoke access with Unity Catalog privileges.
- **Traffic management:** Route requests across model services and MCP services, configure traffic splitting and fallbacks, apply rate limits, and manage budgets with hard spend caps.
- **Runtime guardrails:** Attach service policies to allow, deny, or require approval for interactions based on request and response content. Databricks lists built-in guardrails for PII, prompt injection, and unsafe content.
- **Usage, cost, and audit logging:** Track requests, token usage, latency, requester identity, tags, model destination, and cost through system tables, dashboards, and Unity Catalog Delta inference tables.
- **Databricks-native integration:** Keep governance close to Databricks-hosted models, external models exposed through model services, AI agents, MCP services, and Unity Catalog.

References:

- [Databricks: AI governance with Unity AI Gateway](https://docs.databricks.com/aws/en/ai-gateway/)
- [Databricks: Usage tracking](https://docs.databricks.com/aws/en/ai-gateway/usage-tracking)
- [Databricks: Rate limits](https://docs.databricks.com/aws/en/ai-gateway/rate-limits)
- [Databricks: Inference tables](https://docs.databricks.com/aws/en/ai-gateway/inference-tables)

## GGX value add across automated compliance dimensions

GGX complements a gateway by turning runtime controls and logs into a governed compliance process.

| Compliance dimension           | Databricks AI Gateway contribution                                                                                      | GGX value add                                                                                                                                                                               |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AI inventory and ownership     | AI services can be governed as Unity Catalog securable objects.                                                         | GGX maintains a broader GenAI inventory for models, prompts, RAGs, pipelines, tables, reports, global functions, versions, owners, access scope, and review status.                         |
| Versioning and change control  | Gateway configuration and Unity Catalog permissions govern current service access.                                      | GGX tracks version history, object lineage, challenger comparisons, approvals, and locked production artifacts so reviewers can see what changed and why it was accepted.                   |
| Automated risk identification  | Built-in service policies can detect or block selected runtime risks such as PII, prompt injection, and unsafe content. | GGX maps use-case-specific risks across accuracy, stability, bias, toxicity, vulnerability, privacy leakage, groundedness, hallucination, dark patterns, and agent tool behavior.           |
| Pre-production validation      | Gateway can control which AI services are available and enforce runtime policies.                                       | GGX runs reproducible simulations and comparison jobs against curated datasets, expected outputs, thresholds, and standardized reports before launch.                                       |
| Model risk management evidence | Databricks tables can show usage, requester, tokens, latency, payloads, and policy outcomes.                            | GGX packages evaluation results into dashboards and approval evidence aligned to Model Risk Management, Fair Lending, technology, infosec, legal, and business review workflows.            |
| Fairness and bias testing      | Gateway policies can block or flag selected content patterns at runtime.                                                | GGX supports explicit bias and fairness testing through reusable reports, curated datasets, segment analysis, dashboards, and approval-ready outputs.                                       |
| Human oversight                | Databricks service policies can require approval for selected interactions.                                             | GGX supports human testing, feedback portals, findings workflows, annotation queues, and business SME review loops that turn expert judgment into reusable ground truth.                    |
| Production monitoring          | Gateway usage and inference tables provide operational telemetry and request/response logs.                             | GGX ingests production data, runs monitoring reports, alerts on threshold breaches, routes records for annotation, and turns production findings into new test cases.                       |
| Auditability and documentation | Databricks provides system tables, dashboards, and inference tables inside Unity Catalog.                               | GGX links tests, results, approvals, findings, versions, lineage, and monitoring evidence into an auditable lifecycle record that can be exported or reviewed by committees.                |
| Ecosystem coverage             | Strongest for AI services governed through Databricks and Unity Catalog.                                                | GGX can govern AI applications across multiple providers, agent frameworks, RAG systems, custom pipelines, and production environments, including Databricks where it is part of the stack. |

## When to use both together

Use Databricks AI Gateway and GGX together when Databricks is part of the production AI stack and the organization needs a defensible approval process.

1. **Develop and serve in Databricks:** Use Databricks model services, Unity Catalog permissions, service policies, budgets, rate limits, usage tables, and inference tables.
2. **Register in GGX:** Register the AI application or pipeline, plus relevant models, prompts, RAGs, datasets, and reports.
3. **Evaluate before launch:** Run GGX simulations and comparison jobs for business quality and compliance dimensions.
4. **Approve with evidence:** Attach results to GGX approval workflows for business, risk, compliance, and technical sign-off.
5. **Deploy in databricks:** Export the agent from GGX and deploy it into databricks.
5. **Monitor after launch:** Feed Databricks inference logs or production traces into GGX monitoring dashboards and annotation queues.
6. **Close the loop:** Convert production findings into new test cases, compare challenger versions, and maintain a complete lifecycle record.

## Related GGX docs

- [Inventory Management](../../register-and-refine/inventory-management/)
- [Lineage Tracking](../../register-and-refine/lineage-tracking/)
- [Evaluations and Approval](../../evaluate-and-approve/)
- [Reporting](../../evaluate-and-approve/reporting/)
- [Approval Workflows](../../evaluate-and-approve/approval-workflows/)
- [Deployment and Monitoring](../../deploy-and-monitor/)
- [Annotation Queues](../../deploy-and-monitor/annotation-queues/)
