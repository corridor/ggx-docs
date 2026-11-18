---
title: "Risk Assessment and Compliance"
description: "Record agent risks with inherent and residual severity, attach evidence, check coverage against the EU AI Act, NIST AI RMF, ISO/IEC 42001 and OWASP LLM, and sign the assessment off."
---

Each agent version has a **Risk Assessment** that records how serious each risk is, what mitigates it, and which evidence backs the mitigation. You can also choose the frameworks (laws, standards and guidance) that apply, see how far the assessment covers their requirements, and sign it off.

:::caution
The tier, the coverage and the framework summaries are a guide to help a review. They are not legal advice, and GGX never states that an agent complies with a law or a standard.
:::

## Findings: inherent and residual risk

Every risk has a finding with two severity ratings:

| Rating | Meaning |
|--------|---------|
| **Inherent** | How serious the risk is before any mitigation. |
| **Residual** | How serious it is after the mitigations. |

Both use the same scale: none, low, medium, high, critical. Either may be left empty. When both are set, the residual rating cannot be higher than the inherent one.

A finding also holds the mitigation method, a comment, an open action and its evidence.

## Evidence

Evidence is a record attached to a finding. It can be:

- an evaluation or monitoring job,
- an annotation queue,
- an approval,
- a link (it must start with `http://` or `https://`),
- a note.

Each record belongs to the agent version it was gathered for. When you create a new version, the risk assessment is copied and the old evidence stays visible, marked as **from an earlier version of the agent**. Such evidence is kept but does not count toward coverage until you add fresh evidence for the new version.

## Fill with Corra

**Fill with Corra** reads the agent's prompts, jobs, metrics, approvals and issues, and proposes a mitigation for each risk with the sources it used. It can also propose evidence links for assessed risks that have no recent evidence. You accept or reject each proposal. Nothing is saved until you accept it.

## EU AI Act tier

Answer a short set of yes/no questions to get a tier: **Prohibited**, **High**, **Limited** or **Minimal**. The server computes the tier when you save. Until every question is answered, the assessment shows **Not classified**, never Minimal.

:::note
The questions cover the most common cases only. A **Minimal** result means that none of these questions applied. It does not rule out other obligations, so have a compliance reviewer confirm the tier.
:::

## Frameworks and coverage

Choose which frameworks are in scope for the assessment:

| Framework | Kind |
|-----------|------|
| EU AI Act | Law |
| NIST AI RMF | Guidance |
| ISO/IEC 42001 | Standard |
| OWASP Top 10 for LLM Applications (2025) | Guidance |

Each framework lists requirements. A requirement is linked to one or more **controls**, and a control is linked to the risks of your assessment. One control can serve requirements in several frameworks. Coverage is calculated every time you open the page and is never stored.

**A control is:**

- **Met** when every risk it covers is assessed, has fresh evidence, and has a residual rating of none or low.
- **Partly met** when at least one of those risks is assessed but another condition is not met. A risk with no residual rating counts here.
- **Open** when none of its risks is assessed.

A requirement is met when all its controls are met, open when all are open, and partly met otherwise. Each framework shows how many requirements are met, partly met and open, with the reason for the first problem.

A risk marked only as not applicable needs an explanation to count as assessed.

:::note
Any fresh evidence record counts, including a note. A single note can therefore make a control **Met** when the residual risk is none or low. Review the evidence before you rely on a status.
:::

## Sign off

A person with the **Approve** permission for risk assessments can sign an assessment off once every risk is assessed. A signed-off assessment is read only. Edits, Fill with Corra, restoring a version, deleting and moving it to another project are blocked until someone chooses **Reopen**. The page shows who signed it off and when.

- A copy for a new agent version never comes signed off.
- Deleting an agent version whose assessment is signed off is refused until the assessment is reopened.
- **Approve** is part of the Manage role. To give it to another role, open the role in the project settings and grant Approve on risk assessments. Roles in projects that already exist do not get it automatically.

## Related

- [Approval Workflows](/evaluate-and-approve/approval-workflows/)
- [Agents: risk assessment tab](/register-and-refine/inventory-management/pipelines/#agent-risk-assessment)
