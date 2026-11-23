---
title: "Human Integrated Testing"
description: "Run human-integrated GGX tests where reviewers evaluate agent behavior, capture qualitative feedback, validate outcomes, and support approval decisions."
---

Human Integrated Testing brings people into the loop: reviewers talk to an agent the way its users will, rate each answer, and record what went wrong. It works before approval (to validate a release) and after deployment (to keep checking it).

## What is a test session?

A **test session** is one conversation between a reviewer and an agent in a production-like environment. The session hides the agent's internal steps and shows only the inputs and outputs, so business, risk and clinical reviewers can judge the experience without reading code.

Every message, rating and comment is saved immediately. Sessions are listed under **Human Integrated Testing → Evaluations → Single**, with the agent, the rating, the status and who ran them.

![Evaluations page, Single view: test sessions with their agent, thumbs-up or thumbs-down rating, status and reviewer](./evaluations-single.jpg)

> **Note:** For structured testing by many reviewers, with test definitions, closing questions and insights, use a [Feedback Portal](../feedback-portals/). Sessions run from a portal are listed here too.

## Starting a session

1. Go to **Human Integrated Testing → Evaluations**, switch to **Single** and click **Start Session**. You can also click **Run → Start Chat** on an agent's page.
2. Choose why you are testing:
    - **Business Testing & Feedback**: build ground truth and give feedback on the agent.
    - **Model Development**: check that the agent works while you build it.
3. Choose the agent to test and start chatting.

![Create a new Session dialog: Business Testing & Feedback, or Model Development](./start-session-dialog.jpg)

## During the session

- Rate each answer with 👍 or 👎. A 👎 asks for a reason and a comment.
- Add comments to any message, copy it, or open its menu for more options.
- When you are done, click **Review Session** to record an overall rating and testing notes. Once a session has ended, its chat is read only.

![A completed test session: the reviewer's messages, the agent's answers, and a thumbs-down with a comment on the last answer](./test-session-chat.jpg)

The panel on the left has two views:

- **Information**: the session name, the agent and its version, the feedback portal, a **Feedback Summary** of every rating and comment, and the **Assets** the agent uses (models, sub-agents and prompts, each linked to its page).
- **Configuration**: the settings passed to the agent. They can only be changed where the session allows it.

![The Information panel of a session: agent version, feedback portal, feedback summary with the reviewer's comment, and the models, agents and prompts in use](./test-session-information.jpg)

The **⋮** menu at the top right of a session offers **Debug Mode**, **Edit Session**, **View Events**, **Download Transcript** and **Delete Session**. A session can be run again against the agent; the **Run** selector shows which run you are looking at.

## Benefits

- **Human-in-the-loop testing before approval** of the agent for production.
- An **intuitive chat interface** that hides complex agent logic from business, risk and compliance reviewers.
- **Feedback and ratings on every answer**, rolled up into a summary for the development team.
- **Multi-turn testing** of real-world scenarios.
- **Transcripts** that can be downloaded for documentation or further analysis.

An agent can also be tested and monitored after approval. See [Deploy and Monitor](../../deploy-and-monitor/).
