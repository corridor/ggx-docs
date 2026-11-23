---
title: "Reports and Figures for Annotation Queues"
description: "Build reports of custom charts, tables and summaries from annotation queue data, and choose whether each figure stays live or keeps a snapshot."
---

The **Insights** tab of a queue starts with **Statistics**, the built-in progress charts. For anything else you want to track, such as accuracy by topic or the share of chats the judge and reviewers disagree on, build your own **reports**. A report is a page of figures, and each figure is a chart, a table or a short summary computed from the queue data.

The example on this page is a report called "Accuracy by topic" for a support queue.

## Create a report

In the **Insights** sidebar, under **Reports**, click **Add report** and give it a name. Open the **⋮** menu of a report to **Rename**, **Move up**, **Move down** or **Delete** it.

Figures that were created before reports existed, and sit on no report, are collected in a report called **Custom figures**.

## Add a figure

Open the report and click **Add figure**. Fill in:

- **Name**: what the figure shows, for example "Accuracy by topic".
- **Width**: **Full width** or **Half width**. Two half-width figures sit side by side on a wide screen.
- **Refresh mode**: **Live** or **Snapshot**, described below.
- **Figure Logic**: Python code. It is the body of a function and must `return` a Plotly figure, a Markdown string, or a DataFrame (pandas or polars) that is shown as a table.

The queue data is in the variable `data`, a DuckDB DataFrame, filtered to the date range set at the top of the **Insights** tab. Click **View Examples** for a Plotly, a Markdown and a Table example. Click **Run** (or press Ctrl or Cmd + Enter) to preview the result before you save.

```python
return data.df().groupby("Topic")["Is Accurate"].value_counts().unstack().reset_index()
```

Click **Save**.

## Live or Snapshot

| Refresh mode | When it is computed | Use it for |
| --- | --- | --- |
| **Live** | Every time the report opens, on the current queue data and date range. Shown with a **Live** tag. | Figures that must always match the queue |
| **Snapshot** | Only when you ask. The last result is stored and shown with a **Snapshot** tag and the time it was computed. | Heavy figures, or a view you want to keep fixed for a review |

To update a snapshot, click **Recompute figure** on it. Recomputing uses the date range currently selected on the **Insights** tab.

## Arrange a report

On each figure:

- **Drag to reorder** changes its position.
- **Show at half width** and **Show at full width** switch its width.
- The **Move to another report** button moves it to another report.
- **Edit** and **Delete** change or remove it.

Only people with write access to the queue can add, edit, recompute or reorder figures.
