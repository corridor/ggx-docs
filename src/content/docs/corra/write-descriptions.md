---
title: "Write descriptions"
description: "Let Corra write, add detail to, improve or tweak the description of an agent, prompt, knowledge base, function, dataset, report or model."
---

Corra can draft the **Description** of an asset from what the asset really contains. Use it to get a first draft, to add detail to a short description, or to rework one passage. You always see Corra's proposal first. Nothing changes until you accept it, and even then the form is only edited: save the asset as you always do.

## Where it works

The description editor of these asset types shows the Corra buttons:

- Agents
- Prompts
- Knowledge bases (RAGs)
- Functions
- Datasets (the table description)
- Reports
- Models

The buttons are not shown when the description field is read only.

## What Corra reads

Corra reads the object's content (for an agent, its code and flow; for a prompt, its text; for a dataset, its columns and their descriptions), what the object uses and what uses it, and the description of the project. It does not read the rows of a dataset or the documents of a knowledge base. It leaves out neighbouring assets that you cannot read.

## Write or improve a description

The main button at the bottom right of the editor changes with what is written:

| Description | Button | What Corra does |
|-------------|--------|-----------------|
| Empty | **Write with Corra** | Writes a new description. |
| Short | **Add detail with Corra** | Expands it using what the object contains. |
| Long | **Improve with Corra** | Asks "What should Corra improve?" first. |

For **Improve**, type what to change, or click a suggestion: **Make it shorter**, **Add evidence for facts**, **Add a graphical explanation**. Then click **Improve**.

The sliders button (**Options for Corra**) opens more choices:

- **What should Corra focus on?**: an optional instruction, for example who will read the text.
- **Model**: the provider and model to use.
- **What to do with what is written**: **Improve** keeps what is true and fixes the rest. **Start over** writes a new description and ignores the current one.

## Review the proposal

Corra shows its proposal next to the current text (**Current** and **Corra's proposal**). It may add up to three notes. Choose:

| Button | Effect |
|--------|--------|
| **Accept** | Puts the proposal in the description. |
| **Edit** | Puts it in the description so that you can change it. |
| **Discard** | Throws it away. |

If the request fails, a message appears with **Retry** and **Discard**.

For an agent, Corra also writes a flow diagram under a **Flow** heading in the description.

## Tweak a selected passage

Select text in the description. The bubble menu offers **Tweak with Corra**. Choose "How should Corra tweak this?" by typing an instruction or by picking **Shorter**, **More specific**, **Simpler words** or **Fix mistakes**, then click **Tweak**. Corra rewrites only the selection. Click **Replace** to put it in place of the selection, or **Discard**.

## What Corra will not write

Corra writes plain prose in the present tense. It does not use file paths, links, ids or names of people found in the data, and it does not invent facts, numbers or history that the object does not show. When the current description is already right, Corra may return it unchanged and say so in its notes.
