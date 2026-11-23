---
title: "Finding Issues in Annotation Queues"
description: "Let Corra read an annotation queue for recurring problems, or report them yourself, then triage each issue with evidence, an owner and a status."
---

Reviewing records one by one shows individual mistakes. An **issue** is a problem that shows up across many records, such as "the agent quotes the wrong fee for premium cards". Each issue has a title, a summary, and the records or messages that prove it.

Issues come from two places: reviewers who report them, and Corra, the GGX assistant, which reads the queue and finds them. This page follows one example: a support queue where Corra finds that the agent gives out outdated fees.

## Where issues live

Open a queue, go to the **Insights** tab and select **Issues Found** in the sidebar. The page has an **Open** tab and a **Closed** tab. Search the title or summary, and filter by **Status**, **Found by** (**Corra (AI)** or a person) and **Assignee**.

## Find issues with Corra

Click **Find issues with Corra**. Corra works in waves, one pass through a group of records:

1. **Wave 1** focuses on records with negative ratings from reviewers or the LLM judge, or with comments. Corra reads the conversations and their feedback to see what went wrong.
2. **Wave 2** checks a random sample of up to 200 remaining records for problems nobody flagged. If a wave finds no new issues, the run stops.

While a run works, the page shows its progress, and **Stop** ends it. Each run is listed with the model it used, when it started and ended, and how many issues it found. A run needs a model (see below), and only one run can work on a queue at a time.

New issues start as **Needs review**. If Corra finds more evidence for an issue that already exists, it adds that evidence to the issue.

### Finder settings

Open **Issue finder options** and choose **Finder settings**:

- **Model**: **Use the project's default model**, **Use the organization's default model**, **Use the judge model**, or **Select own** to pick a provider and model. Unless you pick the judge model, the finder signs in with the credentials of the organization's integrations, set under **Platform Settings > Integrations**.
- **Run by itself**: **Off: run only when someone asks**, **Every hour**, **Every week** or **Every month**. Scheduled runs act as the user who saved the settings, so that user needs to stay active with write access to the queue.

### Teach Corra what to look for

Choose **Issue-finding skill** in the same menu. The dialog shows **Platform rules (fixed)**, which every queue follows, and a **Skill** box with your own guidance, for example "treat any mention of a fee as high risk". Click **Save as a new version** to keep the change.

## Report an issue yourself

Click **New issue** and give it a **Title** and **Summary**. A title that matches an existing issue opens that issue instead of creating a duplicate.

To attach a record to an issue while reviewing, right-click the row and choose **Add to issue**, or use **Add to issue** in the chat transcript panel. Pick an issue, or start a new one, and write **Why it is evidence**.

## Work an issue

Select an issue to open it. It has:

- **Status**: **Needs review**, **Open**, **Resolved** or **Won't fix**. **Needs review** and **Open** issues are on the **Open** tab; **Resolved**, **Won't fix** and **Duplicate** issues are on the **Closed** tab.
- **Assignee**: choose a person who can write to the queue, **Assign to me**, or **No one**.
- **Found by**: Corra or the person who reported it.
- **Evidence**: each record or message that shows the problem, with its excerpt. Click **Add evidence** to point at a record by its ID or a copied link, optionally a message number, and say **Why it is evidence**. Mark each piece **Valid** or **Invalid**; the evidence count leaves out invalid pieces.
- **Mark as duplicate**: merge the issue into another one. It then shows as **Duplicate**.
- **Activity**: every change, plus comments. Comments support Markdown.
- **Discuss with Corra**: a chat about the issue, for example whether it is real, what else shows it, or what to do. Corra's answers appear only to you.
- **Links**: **Add to Jira** and **Add to GitHub** link the issue to a ticket in your tracker. **Connect a tracker** appears when none is set up.

**Delete issue** removes the issue with its evidence and activity.
