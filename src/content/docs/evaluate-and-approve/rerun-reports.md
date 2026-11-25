---
title: "Rerun reports and attempts"
description: "Rerun one report or all reports of a finished GGX job on the same output, switch between attempts, add figures to a finished job, and reuse an evaluation's output."
---

A finished job keeps the output that the agent produced. Use that output to run a report again, for example after you fix a report, without running the agent a second time. Each run of a report is saved as an **attempt**, so you can compare and go back.

## Rerun all reports

1. Open a completed job.
2. Click the arrow next to **Rerun** and choose **Rerun All Reports**. The option is disabled until the job is completed and while the job has no report.
3. The form opens with the data locked: *Existing report data will be used. You can't modify the data while rerunning reports.* Check the reports and click **Rerun Reports**.

**Rerun** itself runs the whole job again, agent included. **Rerun All Reports** reuses the output of the existing job.

## Rerun one report

Use this to run a single report again as a new attempt.

1. Open a completed job and select the report tab.
2. Click **Report actions** (the **⋮** button) and choose **Rerun Report**.
3. In **Rerun Report: *evaluation name***, set the report's parameters, if it has any. The dialog says that the report runs again as it is now, on the output of this job, as a new attempt.
4. Click **Rerun Report**.

The report's tab shows the new attempt while it runs. Figures of a finished report can also be run again one at a time: open the menu on a figure and choose **Rerun Figure**, or choose **Rerun All Figures** in the report's **Report actions** menu.

**Rerun Report** is not offered while the job is still running, while another rerun of the same report runs, on a verified job, or when you cannot edit the object. It is also not offered for an evaluation that takes its data from another evaluation.

## Switch between attempts

Once a report has been run more than once, an **Attempt #** button appears beside its actions. While a rerun runs, it reads **Attempt # running…**.

Click the button to list the attempts. Each row shows the attempt number, who ran it and when, and a tag: **Latest**, **Running** or **Failed**.

| Action | What it does |
| --- | --- |
| Click an attempt | Shows that attempt in place of the latest one. The button changes colour and its tooltip says *An earlier attempt is shown*. Click **Latest** to return. |
| **Run new attempt** | At the bottom of the list. Runs the report again. Hidden while an attempt runs, and when you are viewing an earlier one. |
| Trash icon on a row | Deletes an earlier attempt. The confirmation lists what goes with it: for a report, its figures and metrics and the job that ran it. For a figure, the figure and its comment. |

You can delete an attempt only if it is not the latest, the job is not verified, and you ran the job or that attempt.

Figures have attempts of their own, shown with the same button above the figure after it has been run more than once.

## Add an evaluation to a finished job

Add a report on the results of a completed job without running the agent again.

1. In a completed job, click **+** (**Add Evaluation**) beside the report tabs.
2. Enter a **Name** and choose the evaluation to take the data from in **Use data from**. Click **Add**.
3. In the new tab, click **Add Figure**. Describe the chart or table you want under **What do you want to see?** and click **Generate figure**, or pick one of the examples. Corra can use every column of the evaluation output, including columns hidden from **Job Results**.
4. Edit the figure's code directly, or click **Edit with Corra** to change it by chat. Click **Run** to preview and **Save** to keep it. Give the figure a **Name** first.

Existing figures have **Edit** and **Delete** in their menu.

These added reports are called **Inline Reports**. When you rerun the job, the form lists them under **Inline Reports** with a checkbox for each, and an **x of y kept** count. The reports you keep run their figures on the new results when you open the job. Use **Keep all** or **Keep none** to change every report at once.

## Reuse the output of another evaluation

When a job has several evaluations that run the same agent on the same data, you do not need to run the agent for each one.

1. In the job form, open **Evaluation #2** or later and turn on **Reuse the output of another evaluation**.
2. Select the earlier evaluation in **Evaluation whose data to use**.

The agent runs once, for the evaluation you choose. The other evaluation runs only its own report on that output, and its own data settings are turned off.

An evaluation is listed but disabled, with the reason, when it cannot be used. The reasons come from these rules:

- The source must come earlier in the job and must not itself reuse another evaluation's output.
- Both evaluations must have the same agent version, prompt, model or code overrides, input data and settings, such as the evaluation type.
- The report of the reusing evaluation must read only columns that the source's output has.

The switch is available only when you create or rerun a **Simulation** job for an agent, model, prompt or RAG. It is not available in Hillclimb or monitoring jobs, for report jobs, or when rerunning reports.
