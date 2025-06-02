---
title: Prompt Optimization
---

Prompt optimization is the **process of refining prompts** to get better and more accurate responses from AI models. When we create prompts for LLMs to handle complex tasks, the goal is to make intent as clear as possible. However, fully conveying every detail in one attempt is **extremely difficult**. The process often **involves repeated testing and refining, making small adjustments** until the model delivers the desired outcome.

This process of making changes testing impact and maintaining a clear track record of all the experiments can be challenging if done manually. The GGX Platform simplifies and automates this process by introducing **Hill Climbing** Experimentations.

## What is Hill Climbing?

Hill Climbing is a method used to solve optimization problems by gradually improving a solution. It starts with an initial guess and makes small adjustments, keeping any changes that lead to a better result. This process continues until no further improvements can be made, similar to climbing a hill by always moving upward.

## How It Works?

- **Initialization** – Start with an initial prompt.
- **Evaluation** – Run an evaluation using fixed components:
    - Predefined LLM with set hyperparameters
    - Standardized metrics for performance measurement
    - A consistent dataset for testing
- **Modification** – Make small, targeted improvements to the prompt.
- **Comparison** – Rerun the evaluation and measure performance changes.
- **Update** – If the new prompt improves results, it becomes the new baseline.
- **Iteration** – Repeat the process until the desired performance is achieved.

## Benefits of Hill-Climbing Capability:

- The platform maintains **clear logs of all prompt updates** and their impact on model performance.
- Once the best-performing prompt is identified, it can be **synced back** to the base pipeline.
- Enables multiple team members to **collaborate simultaneously** on optimization.
- **Customizable reports** for tracking the Hill-Climbing progress.

> **Note:** The platform also provides flexibility to integrate external prompt optimizers like **[Google Prompt Optimizer](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-optimizer)**.

## How to run Hill Climbing Tasks on Platform?

- Go to object **Details** page.
- Click on the **Run -> Hill Climbing** button.
- **Provide description** about the run.
- **Select Dashboard** to be evaluated in **Dashboard Selection**.
- Make **changes to the prompts** which are part of the object.
- Prepare the data in **Data Sources** which will be used for evaluation.
- Click on **Run** at the bottom and wait for job completion.
- Once the job is completed one can check the optmization progress in Dashboards.
