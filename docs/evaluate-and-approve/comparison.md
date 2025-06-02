---
title: Comparisons
---

Platform provides the ability to compare the registered objects for a specific task using standard and customized metrics. Using this comparison capability one can quickly evaluate a list of candidates to select the best one.

A comparison task typically involves:

- **Current object:** Object which is currently selected and needs to be compared with others.
- **Challenger objects:** Challenger objects are objects of the same type (e.g., models can be
  compared with other models, prompts can be compared with prompts, etc.).
- **Data Source:** A common data source on which objects would be evaluated.
- **Report & Metrices:** Exact evaluation metrics to be compared.

> **Note:** On the platform one can quickly create **Copy** of current objects and change the definitions, swap in swap out components (Like Models, Prompts, Processing etc.) to create challengers.

## How to run a Comparison Task?

- **Register the object and its challenger** versions on the platform.
- Go to the **Details** page of an object to be compared and click on the **Run -> Comparison** button.
- **Provide description** about the comparison run.
- **Select Dashboard** to be evaluated in **Dashboard Selection**.
- Select challenger objects which need to be compared in **Dependencies Section**.
- Prepare the data in **Data Sources** which will be used for evaluation.
- Click on **Run** at the bottom and wait for job completion.

    - Once a job has been submitted it starts in the NEW status
    - The job will go through the following statuses: COMPILING > QUEUED > RUNNING and finally stop at COMPLETED of FAILED

All comparison tasks are systematically recorded on the platform and displayed on the Jobs page of an object in a structured format. They can also be exported as part of the automated documentation process.

> **Note:** The platform allows customizing reports and dashboards specifically for comparison tasks.
> **Note:** Corridor allows running jobs in parallel and multiple threads at a time within a job to expedite the evaluation process.
