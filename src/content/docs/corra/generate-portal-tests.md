---
title: "Generate portal tests"
description: "Let Corra plan and write test chats for a Feedback Portal, run them with an AI caller, and review the results as chats marked Needs review."
---

**Generate tests with Corra AI** writes test chats for a [Feedback Portal](/evaluate-and-approve/feedback-portals/). Corra reads the agent, proposes a plan, writes each test, and GGX runs the chat. Corra writes the tests; it does not play the caller and does not rate anything. The caller is played by GGX's own persona writer and **Auto chat**, and your agent runs exactly as it does in the portal.

## Before you start

You need write access to the portal. Set the stopping field of the portal under **Auto chat settings**, so that a chat can end when its goal is reached.

## Start

1. Open the portal, click **⋮** and choose **Generate tests with Corra AI**. The item is not shown to users without write access, or while the portal is empty.
2. Corra reads the agent's instructions and tools and the lowest-rated chats of this version, then proposes a plan. This can take a moment.
3. Answer the questions Corra asks, such as **Goals and anti-goals**, if they are shown. Corra uses the answers in the plan.
4. Review the plan, then click **Generate N tests**.

A plan that is not started within an hour expires. Click **Open the plan again** to continue. If you change the answers after the plan was made, the dialog says "Answers changed after the plan was made." Click **Plan again**, or **Replan with Corra** at any time.

Click **How it works** for a short explanation of the four steps (Plan, One test at a time, The chat runs, Review).

## The plan

The plan is a table of dimensions. A dimension is a kind of caller, request or risk, for example "Urgent symptoms" or "Out-of-scope requests".

| Column | Meaning |
|--------|---------|
| **Dimension** | The kind of test. |
| **What it checks** | What the tests of that dimension look for. |
| **Cases** | How many tests to write for it. |

Edit any cell, remove a dimension, or click **Add a dimension** to pick a suggestion or **Describe your own**. A plan has at most 12 dimensions, 20 cases in a dimension and 100 tests in total. The dialog shows the total and which version of the agent the tests use.

## Choose the model of Corra

Under **Model of Corra**, pick **Default model of the project**, **Default model of the organization** or **Choose a model**. Corra plans and writes the personas with this model. The callers in the chats are played by the model set in the **Auto chat settings**.

## How each chat ends

Open **How each chat ends**. A chat stops at the first of these. The caller never decides to stop.

| Rule | Setting |
|------|---------|
| The stopping field of the portal is filled | Set in **Auto chat settings**. This means the goal was reached. |
| The agent has replied a number of times | **Replies of the agent** |
| The chat has lasted a number of minutes (the wait for a free kernel does not count) | **Minutes of a chat** |
| The agent errors out | The test is marked **Failed** and its partial chat is kept. |

**Tests at a time** sets how many tests run together, at most 4.

## Follow the run

The **Running tasks** button on the portal opens a drawer with the progress bar and one row for each test: its dimension, title, result and actions. Possible actions are **Stop**, **Skip**, **Open**, **Retry**, **Log** and **Resume**. **Stop all** ends the run. When it ends, **Retry the failed ones** runs the failures again. If the plan is still waiting, **Review the plan** reopens it. Recent runs are listed under **Recent runs** in the dialog, each with **View**. Runs also appear in the [Corra AI drawer](../chat-and-activity/).

## Review the chats

Each finished chat lands in the portal marked **Needs review**. Nothing is rated for you: testers and reviewers rate the chats as they do any other session.
