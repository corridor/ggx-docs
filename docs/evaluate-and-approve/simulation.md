---
title: Simulation
---

The most common type of execution is a **Simulation** - used to execute analytics contained in the definition of an object that has been registered in the platform. And additionally, run dashboards and reports on that output.

A Simulation task typically involves:

- **Current object:** Object which is currently selected and being tested. This can be a Pipeline, Model, RAG, or Prompt.
- **Data Source:** The data to run the object on.
- **Report & Metrices:** Exact evaluation metrics to be run on the output.

## How to run a Simulation Task?

- **Register the object** on the platform.
- Go to the **Details** page of an object to be compared and click on the **Run -> Simulation** button.
- **Provide description** about the run.
- **Select Dashboard** to be evaluated in **Dashboard Selection**.
- Prepare the data in **Data Sources** which will be used for evaluation.
- Click on **Run** at the bottom and wait for job completion.

    - Once a job has been submitted it starts in the NEW status
    - The job will go through the following statuses: COMPILING > QUEUED > RUNNING and finally stop at COMPLETED of FAILED

All simulation tasks are systematically recorded on the platform and displayed on the Jobs page of an object in a structured format. They can also be exported as part of the automated documentation process.

> **Note:** The platform allows customizing reports and dashboards specifically for simulation tasks.
> **Note:** Corridor allows running jobs in parallel and multiple threads at a time within a job to expedite the evaluation process.
