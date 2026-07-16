# Prompt Optimization
Source: https://docs.genguardx.ai/register-and-refine/prompt-optimization/
Markdown: https://docs.genguardx.ai/register-and-refine/prompt-optimization/index.md
Description: How GGX automates prompt optimization with Hill Climbing — iteratively refining a prompt, keeping only changes that improve a fixed evaluation, with full logs and one-click sync back to the pipeline.
Prompt optimization is the process of **refining prompts** to get more accurate responses from an LLM. The goal is to make intent as clear as possible — but conveying every detail in one attempt is hard, so it takes **repeated testing and small adjustments** until the model delivers what you want.

Doing that by hand — making a change, measuring its impact, and keeping a record of every experiment — is tedious and error-prone. GGX automates it with **Hill Climbing** experimentation.

## What is Hill Climbing?

Hill Climbing is an optimization method that improves a solution **gradually**. It starts from an initial guess, makes small changes, and **keeps any change that produces a better result** — like climbing a hill by always stepping upward. It stops when no further improvement can be found.

<figure class="ggx-figure">

![A rising performance curve: from an initial prompt at a low score, each small edit that raises the score is kept and steps up the curve, while edits that lower it are rejected — until the climb reaches the peak, the best prompt.](./hill-climb.svg)

<figcaption>Each kept edit steps the prompt further up the performance curve; edits that score worse are discarded.</figcaption>
</figure>

## How it works

A run holds the evaluation **fixed** and changes **only the prompt**, so any score difference is attributable to the prompt alone.

<figure class="ggx-figure">

![The hill-climbing loop: Initialize, then Evaluate, Modify, Compare, and Update — keeping the new prompt as the baseline only if it scores better — then iterate, with evaluation holding the LLM, metrics, and dataset constant.](./optimization-loop.svg)

<figcaption>Initialize → Evaluate → Compare → Promote → Modify, looping until the target is reached.</figcaption>
</figure>

<Steps>

1. **Initialize** — start with an initial prompt as the baseline.
2. **Evaluate** — score it against fixed components: a predefined **LLM with set hyperparameters**, **standardized metrics**, and a **consistent dataset**.
3. **Modify** — make a small, targeted change to the prompt.
4. **Compare** — re-run the evaluation and measure the change in performance.
5. **Promote** — if the new prompt scores better, it becomes the new baseline; if not, it is discarded.
6. **Iterate** — repeat until the desired performance is reached.

</Steps>

<Aside type="note" title="Why hold everything else constant">
Fixing the LLM, the metrics, and the dataset is what makes the comparison fair: when only the prompt changes, a higher score can be credited to the prompt and nothing else.
</Aside>

## What the capability gives you

| Benefit | What you get |
|---------|--------------|
| **Full experiment log** | Every prompt update and its impact on performance is recorded automatically. |
| **One-click sync-back** | Once the best-performing prompt is found, sync it back to the base pipeline. |
| **Team collaboration** | Multiple members can work on the same optimization simultaneously. |
| **Custom reports** | Configurable dashboards and reports track hill-climbing progress over time. |

<LinkCard
  title="Bring your own optimizer"
  description="GGX can also integrate external prompt optimizers such as Google's Vertex AI Prompt Optimizer."
  href="https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-optimizer"
/>

## Running a Hill-Climbing task

<Steps>

1. Open the object's **Details** page.
2. Click **Run → Hill Climbing**.
3. **Provide a description** of the run.
4. Under **Dashboard Selection**, choose the dashboard to evaluate against.
5. Make the **changes to the prompts** that are part of the object.
6. Prepare the evaluation data under **Data Sources**.
7. Click **Run** and wait for the job to complete.
8. When it finishes, review the optimization progress in the **Dashboards**.

</Steps>

:::tip[Start from your best prompt]
Hill climbing builds on the baseline, so a stronger starting point reaches a higher peak in fewer iterations.
:::