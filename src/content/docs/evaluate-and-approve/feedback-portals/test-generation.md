---
title: "Generate tests with Corra"
description: "Let Corra plan and run a set of tests for an agent in a GGX Feedback Portal, review the plan, follow the run, and retry the tests that fail."
---

Corra can write a set of tests for the agent behind a [Feedback Portal](../), run each one as a chat, and put the chats in the portal for review. You review the plan before anything runs.

## How it works

1. **Plan.** Corra reads the agent's instructions, tools and its lowest-rated chats, and proposes dimensions with the number of tests each needs. You review the plan.
2. **One test at a time.** For each test Corra writes the scenario, the goal, the caller's persona and the first message.
3. **The chat runs.** The portal's [Auto chat](../#auto-chat) continues from the first message. Corra writes the tests; it does not play the caller.
4. **Review.** Each chat lands in the portal tagged **Corra** and **Needs review**, and **Reviewed** after the session is ended. Nothing is rated for you.

## Start a run

You need write access to the portal.

1. Open the portal and choose **⋮ → Generate tests with Corra AI**. On a portal with no tests, click **Generate tests**.
2. In **Generate tests with Corra AI**, choose the **Model of Corra**: **Default model of the project**, **Default model of the organization** or **Choose a model**. Corra plans and writes the personas with this model. The callers in the chats use the model in the [Auto chat](../#auto-chat) settings.
3. Wait while Corra reads the agent, then review the plan.
4. Click **Generate** *N* **tests**.

## Review the plan

The plan is a table with one row per dimension, which is a kind of case to cover.

| Column | What to do |
| --- | --- |
| **Dimension** | Name the area, for example a type of request. |
| **What it checks** | Describe what the tests in this dimension look for. |
| **Cases** | Set how many tests to write. At least 1. |

Click the **x** to remove a dimension. Click **Add a dimension** to pick one of Corra's suggestions or **Describe your own**. Click **Replan with Corra** to get a new plan. The total of tests and the agent version the tests use are shown under the table.

A plan has at most 12 dimensions, 20 cases per dimension and 100 tests in all. If you do not generate within an hour, the plan expires and you can click **Open the plan again**.

### How each chat ends

Open **How each chat ends** to set the limits. A chat stops at the first of these:

| Limit | Meaning |
| --- | --- |
| Stopping field | The agent's context has a stopping field from the Auto chat settings. The goal is reached. |
| Replies of the agent | The agent has replied this many times (default 8). |
| Minutes of a chat | The chat has lasted this long, not counting the wait for a free kernel (default 4). |
| Agent error | The test is marked **Failed** and its partial chat is kept. |

**Tests at a time** sets how many run in parallel, up to 4.

## Follow the run

The tasks control at the top of the portal opens the **Running tasks** drawer, and it opens by itself after you start a run. It shows the progress, one row per test with its dimension, title and result, and a **Stop all** button. Click **Review the plan** there if the plan is still waiting for you.

Each row has actions that depend on its state:

| Action | When |
| --- | --- |
| **Skip** | The test is waiting. |
| **Stop** | The test is running. |
| **Open** | The test has a chat. |
| **Retry** | The test failed. |
| **Log** | The test has a log. |
| **Resume** | The test was stopped. |

When the run ends, **Retry the failed ones** runs the failed tests again. Tests that failed with an agent error keep their partial chat in the portal.
