---
title: "Testing plan"
description: "Plan the testing of a GGX Feedback Portal in four steps: what to cover, which personas chat, who tests which values, and when testing is due."
---

A **testing plan** says what a team of testers must cover in a [Feedback Portal](../), who covers what, and by when. The wizard works out the number of tests and the time they take from your choices.

## Open the wizard

You need write access to the portal.

- On a portal with no tests, click **Set up a testing plan**.
- On any portal, choose **⋮ → Edit testing plan**. The dialog is titled **Create your testing plan**, or **Edit your testing plan** once a plan exists.

Use **Next** and **Back**, or click a step you have already reached. **Finish** saves the plan. Next is off until the step is valid, and the footer says what is missing. The **Plan so far** panel on the left shows the running totals: **Dimensions**, **Personas**, **Values to cover**, **Total tests**, **Testers** and **Total time**.

## Step 1: Coverage

*What the agent is tested on.* A **dimension** is a way the tests should vary, such as the topic of the request, with a list of values.

1. Under **Add a dimension**, tick the dimensions to include. Templates are provided: **Intent**, **Language**, **User tone**, **Ambiguity**, **Out-of-scope request** and **Safety-critical case**. You can change the values afterwards. Click **Create empty dimension** to start from nothing.
2. For each dimension, complete the sentence **Test** *name*, **prioritised by** *how*, **taking** *which values*.

| Prioritised by | Meaning |
| --- | --- |
| **equal importance** | Every value counts the same. |
| **volume** | The values that occur most often come first. You can upload volumes. |
| **importance I set** | You mark each value High, Normal or Low, and the High ones come first. |

For **taking**, choose **All values** or **The top N by priority** and set **How many**. The count under the sentence shows how many values are left out.

3. Edit the values with **Add one value**, **Add multiple**, **Upload CSV or Excel**, or search them with **Search**.

## Step 2: Test Scenarios

*Who is chatting with the agent.* A persona is a kind of person who chats with the agent, such as a worried parent. Tick the personas to cover. This step is optional. Click **Add a persona** to write a **Name** and **Description**; a persona added here is added to the agent too. Personas do not multiply the number of tests.

## Step 3: Execution Owners

*Who tests which values.*

1. Click **Add tester** and choose people. The step needs at least one tester.
2. For each dimension, choose the testers who take it and how to split it:

| Split | Meaning |
| --- | --- |
| **blocks of 10** | Blocks of 10 values dealt to the testers in turn. |
| **equal shares** | One contiguous share each. |
| **tested by everyone** | Every tester covers all the values. |
| **custom ranges** | Choose the positions or values of each tester. |

**Split everything evenly** applies an even split to every dimension. A note shows how many values still have no tester. Switch between **By dimension** and **By owner** to see the same assignment from either side.

## Step 4: Time Window

*When the testing is due.* Set **Start date**, **Due date** (or *anytime*) and the reminders: **never**, **weekly on Monday**, **daily** or **only when behind**. Set **Time per test** in seconds; it sets the estimated work of each tester. The table shows each tester's estimated work and target per day or per week.

Dates and reminders are saved with the plan. GGX does not send reminders yet.
