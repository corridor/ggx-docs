---
title: "Comparisons"
description: "Compare GGX objects against challengers using shared datasets, selected metrics, automated reports, and side-by-side results for model and agent evaluation."
---

GGX can compare results on the same task, with standard and customized metrics, so you can quickly pick the best of several candidates. There are two ways to compare:

- **Comparison** opens two completed jobs side by side. It does not run a new job.
- **Hillclimb** keeps the agent as it is but changes its prompts, one or more of its attached models, or the Code Repo branch it runs, and compares the result with a baseline job.

> **Note:** Use **Copy** or **Clone** on an object to create a challenger quickly, then change its definition or swap components such as models, prompts or processing. Run a [Simulation](../simulation/) of each, then compare the two jobs.

## How to run a Comparison

1. Run a [Simulation](../simulation/) for each version you want to compare and wait for both to be **COMPLETED**.
2. Open the object's page and click **Run → Comparison**.
3. In **Comparison Configuration**, answer **Do you have 2 completed jobs to compare?** with **Yes**. If you answer **No**, click **Run a Job** to start a Simulation first.
4. Choose the **Left Job** and the **Right Job**. They must be different jobs.
5. Click **Start Comparison**.

You can also open a completed job, click **⋮ → Compare with other Simulation** and choose the job to compare it with. Choose **Stop Comparison** from the same menu to go back.

## Hillclimb: change an agent and compare

**Hillclimb** answers questions like *"Can we move to a lighter model without losing quality?"* or *"Does this prompt do better?"*. It reruns the baseline job's evaluations with the changes you make. It is available for agents.

1. Run a [Simulation](../simulation/) of the agent as it is. This is the baseline.
2. Click **Run → Hillclimb** on the agent, answer **Do you have a base job?** with **Yes**, choose the completed job and click **Start Hillclimb**. If you answer **No**, click **Run base Job** to create one first. You can also open a completed job and click **Hillclimb**.
3. Make one or more changes in the panels below.
4. Keep the same evaluations and data, and click **Run Job**.

### What you can change

| Panel | What you can do |
| --- | --- |
| **Models** | Replace any attached model with another model from the catalogue. Click **Revert** on one model, or **Revert All**. The panel only appears when the agent has attached models. |
| **Code Repo** | For an agent that runs code from a Code Repo: choose another branch to run. The job runs the commit the branch is at when it starts. The panel shows **Branch changed** until you click **Revert**. |
| **Prompts** | Edit the text of any prompt the agent uses. Click **Add prompt** to include another prompt, the sync icon to reset a prompt to its registered text, and the trash icon to remove it. |

These changes apply to this job only. They do not change the registered agent, model or prompt.

The results open side by side with the baseline, report by report, so a metric that moved is easy to spot. Use the selector at the top to choose which job to compare against.

![Hillclimb results: the baseline and the lighter-model run side by side, with the probes below their target in red](./hillclimb-side-by-side.jpg)

The Job Details of a hillclimb job list the models that were replaced, for example *1 model · 1 replaced*. On a finished hillclimb job, the prompts show as a difference against the registered text.

All comparison and hillclimb jobs are recorded on the platform, shown on the object's **Jobs** tab and under **Human Integrated Testing → Evaluations → Batch**, and can be exported as part of the automated documentation.

> **Note:** Reports and dashboards can be customized for comparison tasks. See [Reporting](../reporting/).
>
> **Note:** GGX runs jobs in parallel, and runs several rows at a time within a job (the **Execution Concurrency**), to speed up evaluation.
