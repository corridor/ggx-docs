---
title: "Lineage Tracking"
description: "Use GGX lineage tracking to visualize object dependencies, trace upstream and downstream impact, and see how registered assets are used."
---

Lineage tracking records and visualizes the complete lifecycle of an object and depicts the flow of execution, showing how objects interact, are transformed and executed. It captures its origins, building blocks used, transformations, and usages across the organization.

## Why Lineage Tracking is Important?

- **Ensures Traceability** by providing a clear link between all artefacts, ensuring transparency in dependencies and usages.
- **Easier Impact Assessment** for modifications.
  - Provides a clear view of all dependent objects that would be affected by changes.
  - Identifies necessary updates across dependencies to introduce changes.
- **Enhances Collaboration** by providing visibility into how different teams and models interact within the agent.
- **Ensures Compliance** with regulations like the **[EU AI Act (Article 13 & 14)](https://eur-lex.europa.eu/resource.html?uri=cellar:e0649735-a372-11eb-9585-01aa75ed71a1.0001.02/DOC_1&format=PDF)**, which mandates transparency and human oversight.
- **Identifying redundant processes**.

## Lineage Structure on GGX Platform:

A lineage is created and automatically maintained by the platform as soon as an object is registered. It appears in the **Lineage** section at the bottom of the object's **Details** tab, as a horizontal tree that maps how the object is built and where it is used.

The section has two views. Pick **List** or **Graph** with the switch at the top right.

| View | What it shows |
| --- | --- |
| **Graph** | A tree of how the object is built and where it is used. A second switch picks **Precedents** or **Dependents**. |
| **List** | What the object uses (its precedents), grouped by type. |

### Graph view

- **Precedents**: the sources and dependencies the object is built from, such as the prompts, models, RAGs and sub-agents of an agent.
- **Dependents**: the other objects that rely on this one. For an agent, this includes the deployments that run it.

The legend at the top counts the objects of each type in the graph (for example *Pipeline (10)*, *Prompt (10)*, *Model (2)*, *RAG (2)*); open a type to find a specific object. Use the controls at the top right to change the layout, refresh or search, and zoom with the controls at the bottom right. Click a node to see its details and open it.

![The Lineage section of an agent, Precedents view: the prompts, models and sub-agents the General Hospital Care Companion is built from](./lineage.jpg)

## List view and export

The **List** view groups what the object uses under these headings: **LLMs / Models**, **Prompts**, **RAGs**, **Sub-Agents**, **Helper Functions**, **Datasets** and **Reports**. A group with nothing in it is left out. Each row shows the object's name, version and status. Click a row to open its details, or use the arrow next to a row to show or hide what that object uses in turn.

Click **Export** to save everything the object uses, including rows you have collapsed, as one of:

- **JSON (nested tree)**
- **Markdown outline**

The file is named after the object, for example `card_assistant-lineage.json`.

## Assets detected in agent code

An agent that runs from a [Code Repo](../inventory-management/#code-repos) can use models, prompts, tools, knowledge sources and other agents that are written in its code and not registered in GGX. GGX reads the code at the commit the agent runs and lists what it finds under the agent's precedents.

Detected assets are different from registered objects:

- They are marked as detected, with their own icon for the kind of asset, and in the list they sit in the group of the matching type (a detected tool under **Helper Functions**, a detected model under **LLMs / Models**).
- They have no page, version or status, because they are not objects in GGX.
- They never count in an approval check. Only registered objects do.
- They appear among precedents only, never among dependents.

Click a detected asset to open its details:

| Detail | What it tells you |
| --- | --- |
| **Source** | That the asset was detected in the code and is not registered in GGX. |
| **Detected as** | The kind and how it is built, for example a tool that is a function, or a model and its provider. |
| File and location | The file and lines where it is defined, with a link that opens the file in the Code Repo at the detected commit. |
| Value | A model name or prompt text, when the code states it. When it does not, the reason is shown after **Not known**, for example that the value is set by an environment variable or built when the code runs. GGX does not guess. |
| Definition | The code of a tool or agent. Long definitions are cut; open the file for the rest. |

An asset that is registered in GGX as the same thing is shown as the registered object instead.
