---
title: Prompt Registry
---

<helper-panel object='Prompt' location='list'>

## What is a Prompt?

A prompt is a natural language instruction provided to a generative model to direct its response or produce a desired outcome. It may include questions, commands, contextual details, few-shot examples, or partial inputs for the model to complete or extend.

A prompt typically includes:

- **Prompt Template:** An instruction containing placeholders.
- **Input Arguments:** Dynamic inputs that replace the placeholders.

**Note:** System prompts might not always have Input Arguments.

Additionally, to generate the prompt using the template and input arguments, there should be a:

- **Creation Logic:** Code that generates, retrieves, or formats the input arguments and fills them into the template.

> **Note:** If a prompt contains no processing or formatting logic, the creation logic can directly return the prompt template.

![What is a Prompt?](./prompt-concept.excalidraw.svg)

## Managing Prompts on the Platform:

The **Prompt Registry** organizes all the registered prompts into customized groups at this centralized location and allows easier tracking, monitoring, and creating new ones.

### Registering a Prompt:

1. Click on **Create** button in Prompt Registry.
2. Fill in important details like **Name**, **Attributes** (alias), **Properties** (Description, Group, Permissible Purpose, Approval Workflow).
3. **Select registered resources** (like Model, Global Functions, etc.) which can help with prompt creation. These resources can be used in the prompt creation logic section.
4. Define the **Input Arguments**, **Prompt Template**, **Prompt Creation Logic**.
5. **Add notes**, **attach documentation** if available in the **Additional Information** section.
6. Lastly, click on the **Save** button to complete the registration process.

The registered prompts can be evaluated in the Prompt Registry or can be used in downstream objects (like RAG, Model, Pipeline, Reports, etc.).

## Benefits of Prompt Registration:

- Automated tracking and **recording of modifications** with efficient version upgrades.
- Automatic detection of **Permissible Purpose violations**.
- Perform **evaluations** using standardized and custom validation kits.
- **Enhances reusability** across downstream applications and enables usage tracking with **Lineage Tracking**.
- Journey to production becomes more **transparent and fully auditable**, and **production monitoring** gets easier.
- Extract ready-to-productionize **executable artifact**.

</helper-panel>
