---
title: "Get feedback from an expert"
description: "Send chats from a completed GGX agent job to a Feedback Portal so reviewers can read, rate and comment on them as test sessions."
---

Use **Get Feedback from Expert** to hand chats from an evaluation to the people who can judge them. Each chat becomes a session in a [Feedback Portal](../feedback-portals/), where reviewers rate the answers and end the session like any other.

## Before you start

- The job ran an **agent**. Results of other objects cannot be sent.
- The job is **COMPLETED**. Until then the action is disabled with the tooltip *Available when the job is completed*.
- You are working inside a project that has a feedback portal you can write to.

## Send chats

1. Open the job and go to **Job Results**, or to a report tab that lists the rows.
2. Open a row, or right-click it in the table, and click **Get Feedback from Expert**. In the row view the button is at the top, beside the view selector.
3. In the **Get Feedback from Expert** dialog, select the portal. Portals that you can only read are listed but cannot be chosen.
4. Click **Send to the portal**.

A confirmation says how many chats were sent and links to the portal's sessions with **Go to feedback portal**.

## What is sent

A row counts as a chat when it comes from a multi-turn evaluation, or from a single-turn run of a chat agent with a user message and an answer. Rows from an annotation queue and rows with an error and no answer are not offered.

Each chat is sent as a new session that is not ended, so reviewers can rate it and end it. The session records which evaluation and record it came from, so:

- A chat that the portal already has from this job is skipped (*already sent*).
- A chat with no messages is left out.
- Images and files in a chat that a session cannot keep, such as audio, are left out. The confirmation counts them.
