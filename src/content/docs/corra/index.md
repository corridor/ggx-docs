---
title: "Corra AI"
description: "Corra is the AI assistant built into GGX. See where it appears, what it can do, who can use it and which models and permissions it works with."
---

**Corra** is the AI assistant built into GGX. It answers questions in a chat, writes descriptions of your assets, proposes answers for a risk assessment, writes test chats for a Feedback Portal, finds recurring problems in your data, and creates a project from a description. In the app it is called **Corra AI**.

Corra proposes; people decide. Descriptions, risk assessment fills and test plans are saved or run only after a person accepts them. The exceptions are issue finding, which adds issues marked **Needs review**, and test generation, which adds chats marked **Needs review**.

## Where Corra appears

| Where | What you see | Page |
|-------|--------------|------|
| Top bar | A sparkle button named **Corra AI**. It opens a drawer with your runs and chats, and from there a chat panel. | [Chat and activity](chat-and-activity/) |
| Description of an agent, prompt, knowledge base (RAG), function, dataset, report or model | **Write with Corra**, **Add detail with Corra** or **Improve with Corra** | [Write descriptions](write-descriptions/) |
| An agent's **Risk Assessment** tab | **Fill with Corra** | [Fill a risk assessment](fill-risk-assessments/) |
| A Feedback Portal | **⋮ → Generate tests with Corra AI** | [Generate portal tests](generate-portal-tests/) |
| Issues in an annotation queue or a Feedback Portal | **Find issues with Corra**, **Discuss with Corra** | [Discuss issues and tweak results](discuss-and-tweak/) |
| Prompt analysis, and the figures of a job report | **Tweak this analysis with Corra**, **Edit with Corra** | [Discuss issues and tweak results](discuss-and-tweak/) |
| Project list, **Create** dialog | **Create project with Corra AI (needs root mode)** | [Create a project](create-a-project/) |
| Account menu → **Corra MCP** | Setup for connecting an AI client to GGX | [Corra MCP settings](corra-mcp/) |

For finding issues in a queue, see [Finding issues](/deploy-and-monitor/annotation-queue-issues/). For Corra-written scenarios and **Discuss with Corra** in a portal, see [Feedback Portals](/evaluate-and-approve/feedback-portals/). For the risk assessment itself, see [Risk Assessment and Compliance](/evaluate-and-approve/risk-assessment/).

## What Corra can and cannot do

Corra can:

- Read the asset or the evidence a feature is about, and write text or a proposal from it.
- Work in the background on longer jobs (a risk assessment fill, test generation, issue finding, project creation) while you carry on. These jobs show in the Corra AI drawer.
- Show the sources it used for a risk assessment proposal, and the evidence for an issue.

Corra cannot:

- Change an object on its own. You accept a description, a proposal or a step, or approve a change in a discussion, before anything is saved.
- Answer from your data in the general chat. The chat in the top bar has no tools: it answers from what it knows about GGX and from what you type.
- Rate chats in a Feedback Portal. Corra writes and runs the tests, and people review them.
- Write the summary of the **AI Policy**. **Generate with Corra** on that page is switched off and shows "Coming soon: Corra will write the summary from your PDFs."

:::caution
Corra can make mistakes. The chat panel says so under the message box: "AI can make mistakes, so double check it." Check what Corra proposes, especially in a risk assessment.
:::

## Who can use Corra

There is no separate Corra permission. Each feature follows the permissions on the object it works on:

| Feature | Who can use it |
|---------|----------------|
| General chat, activity drawer | Any signed-in user. The drawer lists only your own runs and chats. |
| Write, improve or tweak a description | Whoever can edit the description of that object. The option is not offered when the field is read only. |
| Fill with Corra | Whoever can edit the risk assessment. The button is not shown otherwise. |
| Generate tests with Corra AI | Whoever can write to the Feedback Portal. |
| Discuss with Corra | Whoever can read the issue or the portal. Having Corra add evidence or a comment needs write access. |
| Edit a figure with Corra | Whoever can edit the object the job ran on. |
| Tweak a prompt analysis | Whoever can read the prompt. |
| Create project with Corra AI | An organization administrator only. |

Corra reads only what you may read. When it writes a description, it leaves out neighbouring assets that you cannot read.

## Which model Corra uses

Corra runs on the language model integrations your organization has set up under **Platform Settings → Integrations**. It does not bring a model of its own. See [Platform settings](/administration/platform-settings/) and [Integrations](/integrations/).

- The general chat and most features use the integrations of the project you are working in: the project's own integration for a provider it overrides, and the organization's otherwise. The chat shows a **Model** picker.
- Fill with Corra and test generation let you choose where the model comes from: **Use the project's default model**, **Use the organization's default model**, or your own choice (**Select own** in Fill with Corra, **Choose a model** in test generation).
- With no usable integration, a Corra feature stops with an error such as "No supported integrations found. Configure integrations in Platform Settings to use AI features."

Corra signs in to the model with the credentials of your organization's integrations.
