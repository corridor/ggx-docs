---
title: "Fill a risk assessment"
description: "Let Corra read the evidence about an agent and propose risks and mitigations for its risk assessment, then accept or reject each proposal."
---

**Fill with Corra** is a button on an agent's **Risk Assessment** tab. Corra reads the evidence your project holds about the agent and proposes how each open risk is mitigated and how much risk is left. It can also suggest risks the assessment does not list. You decide on every item. This page explains the run, the review and the two settings behind it. For the assessment itself, see [Risk Assessment and Compliance](/evaluate-and-approve/risk-assessment/).

## What Corra reads

Corra reads the assessment as it stands, and the evidence about the agent version it covers:

- The agent and its prompts.
- The jobs run on it, with their metrics and figures.
- The approvals and what reviewers asked or granted.
- The issues in the annotation queues those jobs used.

It reads these as pages of text made when the run starts. It cannot change the assessment while it works. Anything written in a prompt, comment or issue is treated as data to report on, never as an instruction.

For each risk that is **not assessed**, Corra decides whether the evidence is enough. If it is, it proposes:

| Proposal field | Meaning |
|----------------|---------|
| **Mitigated by** | One or more mitigation methods that a page shows to be in place. |
| **Residual risk** | The severity left after the mitigations, with a reason. |
| **Open action** | What a person should do next. It is left out when nothing is open. |
| **Based on** | The pages used, each with a note of the words or the number that support the item. |

If the evidence is too thin, Corra leaves the risk out and names it in its notes, with what would give the evidence, such as a job to run or a prompt to add. Corra is told to stay consistent with risks a person already assessed, and to propose at most five new risks, each with a reason and its evidence.

## Run a fill

1. Open the agent's **Risk Assessment** tab. Save any unsaved changes first: the button is disabled with the hint "Save your changes first" until you do.
2. Click **Fill with Corra**. The button needs write access to the assessment.
3. A dialog titled **Fill the assessment with Corra** shows what Corra is doing, in a sentence. The run takes a few minutes.
4. Close the dialog if you wish and carry on. The button changes to **Corra is working…**, and to **Review the proposal** when the proposal is ready, also after you reload the page.

Click **Stop** in the dialog to cancel the run. Only one run can work on an assessment at a time. The run also appears in the [Corra AI drawer](../chat-and-activity/).

A run that ends without a proposal shows its reason, with **Try again**.

## Review the proposal

The dialog lists each item with the tag **Suggested by Corra**:

- **Fill**: a mitigation and residual risk for a risk that is not assessed yet.
- **New risk** or **New category and risk**: a risk the assessment does not list.

Each item shows its explanation and its **Based on** sources. Corra's notes appear above the list. For each item click **Accept** or **Reject**, or use **Accept all** and **Reject all**. The dialog counts "N accepted, N rejected, N to decide".

Click **Save N accepted** to write the accepted items to the assessment. They stay marked as suggested by Corra. Items you reject or leave undecided are not saved. **Discard the proposal** closes the review and saves nothing, and **Close without saving** keeps the proposal so you can come back to it.

If every risk is assessed, or the evidence says too little, the dialog says "Corra has nothing to propose".

## Choose the model

Click the **⋮** menu next to the button and choose **Filler settings**. Under **Model**, pick:

- **Use the project's default model**
- **Use the organization's default model**
- **Select own**: choose a provider and a model

Click **Save**. The next run uses it. Corra signs in with the credentials of the organization's integrations, which you set up under **Platform Settings → Integrations**. A model whose provider is not set up is refused, and nothing is saved.

## Tell Corra how to investigate

Choose **Risk Filling skill** in the same menu. The dialog is titled "Instructions of Corra for this assessment". It holds markdown that tells Corra how to investigate the evidence and how to rate a risk. Open **Platform rules (fixed)** to read the rules every assessment follows. They come before your text and you cannot edit them.

Edit the text and click **Save as a new version**. The next run reads it. The dialog shows the current version.
