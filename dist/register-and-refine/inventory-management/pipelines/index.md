# Pipelines
Source: https://docs.genguardx.ai/register-and-refine/inventory-management/pipelines/
Markdown: https://docs.genguardx.ai/register-and-refine/inventory-management/pipelines/index.md
Description: How pipelines work in GGX — compose Models, RAGs, Prompts and Guardrails with orchestration logic. Covers pipeline types, anatomy, registration steps, testing, and risk assessment.
<helper-panel object='Pipeline' location='list'>

## What is a pipeline?

A **pipeline** is how you turn individual building blocks into a working GenAI application in GGX. It wires reusable components — Models, RAGs, Prompts, Guardrails, and even other pipelines — together with a piece of orchestration code, then takes an input, runs it through that logic, and returns a generated or predicted output.

:::tip[A simple way to picture it]
Think of a pipeline as a **recipe**: the registered components are the ingredients, and the **orchestration logic** is the set of instructions that decides how they combine.
:::

## A worked example: an IVR assistant

Consider an **IVR (Interactive Voice Response)** assistant that automates customer support calls. Rather than building it as one large block of logic, you compose it from two smaller, reusable sub-pipelines.

<figure class="ggx-figure">

![Flow of an IVR pipeline: a caller message passes through Intent Classification then Response Generation to produce a spoken reply.](./ivr-pipeline-flow.svg)

<figcaption>The IVR pipeline orchestrates two reusable sub-pipelines in sequence.</figcaption>
</figure>

The IVR pipeline simply orchestrates the two in order:

<Steps>

1. The caller's message arrives.
2. **Intent Classification** labels the intent.
3. **Response Generation** uses that intent to produce the final reply.

</Steps>

Because each sub-pipeline is registered on its own, you can reuse it elsewhere — the same Intent Classification sub-pipeline could power a chat widget or an email-triage tool.

:::note[End-to-end flow]
1. Caller says: *"I lost my credit card."*
2. Intent Classification (LLM + Prompt) returns intent: `Report Lost Card`.
3. Response Generation (LLM + Prompt + RAG) replies: *"I'm sorry to hear that. I've blocked your card. Would you like a replacement?"*
:::

## The three pipeline types

Every pipeline in GGX is one of three types. Choosing the right one is the first real decision you make when registering — it determines how the pipeline handles memory and what shape its output takes.

<Tabs>
<TabItem label="Chat-Based">

<Badge text="Stateful" variant="tip" /> **Best for** conversations, assistants, and multi-turn support.

- Keeps `history` and `context` across turns
- Stays aware of an ongoing conversation
- Output is fixed: `{"output": ..., "context": ...}`

*Example:* a support chatbot that recalls earlier messages.

</TabItem>
<TabItem label="Free-Flow">

<Badge text="Stateless" variant="note" /> **Best for** one-shot generative tasks — summarization, drafting, extraction.

- No memory — each input is independent
- Processes one input and is done
- Output shape is whatever you define

*Example:* a pipeline that summarizes a document in a single pass.

</TabItem>
<TabItem label="Classification">

<Badge text="Fixed labels" variant="success" /> **Best for** sorting an input into a known category — sentiment, intent, routing.

- Returns one label from a set you predefine
- Can run single-turn, or take prior `context`
- Output is a fixed label, e.g. `positive`

*Example:* a pipeline that labels a review as `positive` or `negative`.

</TabItem>
</Tabs>

:::tip[Which should I choose?]
Pick **Chat-Based** for a back-and-forth conversation, **Classification** when the answer must be one of a fixed set of labels, and **Free-Flow** for any other one-shot task.
:::

## Anatomy of a pipeline

Regardless of type, every pipeline has the same three-part shape: it receives **inputs**, runs **scoring logic** that draws on **registered resources**, and returns an **output**.

<figure class="ggx-figure">

![Pipeline anatomy: an input flows into scoring logic, which draws on registered resources, and returns an output.](./pipeline-anatomy.svg)

<figcaption>Inputs flow into scoring logic, which calls on registered resources to produce an output.</figcaption>
</figure>

:::note
For chat pipelines, the returned `context` is fed back in on the next turn — that is how the pipeline stays aware of an ongoing conversation.
:::

## Adding a pipeline to the registry

The **Pipeline Registry** is the central place where all registered pipelines live, organized into customizable groups. From here you can track, monitor, test, and create pipelines. There are two ways to add one:

<CardGrid>
<Card title="Create from scratch" icon="add-document">
Build the logic directly in GGX with the Python Function Editor. A transparent, white-box approach: every component is registered inside GGX and stitched together, so each can be independently tested, validated, and debugged.
</Card>
<Card title="Connect an external agent" icon="comment-alt">
Integrate a pipeline already running elsewhere through its API. A black-box approach where the agent's internals are abstracted away and interaction is limited to invoking it and consuming its outputs.
</Card>
</CardGrid>

## Registering a pipeline from scratch

Click **Create** on the Pipeline Registry page, then work through the registration form:

<Steps>

1. **Name and description.** Give the pipeline a clear name, then a plain-English description of what it does, when to use it, and when not to — it is what teammates read when deciding whether to reuse it. Under **Add Additional Details**, set the **Group**, **Permissible Purpose**, and metadata like **Usecase Type** and **Task Type**.

2. **Alias.** <Badge text="required" variant="caution" /> A code-safe variable name other pipelines use to refer to this one — lowercase with underscores, no spaces. For our running example: `card_assistant`.

3. **Input type.** Choose how the logic is supplied:
   - **Python Function** — write the logic in the Scoring Logic editor on this page.
   - **External Agent** — connect to an agent built elsewhere.

4. **Pipeline, interaction, and context type.** These three move together:
   - **Pipeline Type** — pick **Chat-Based**, **Free-Flow**, or **Classification**.
   - **Interaction Type** — set automatically from Pipeline Type; for chat it is `TypedDict[{'role': str, 'content': str}]`.
   - **Context Type** — required for chat pipelines; the data type of the `context` carried between turns, e.g. `dict[str, str]`.

5. **Config, resources, and model file.** Attach what the logic needs:
   - **Add Config** — input arguments or configuration values, each with a type and default.
   - **Add Resources** — registered Models, Prompts, RAGs, Global Functions, Guardrails, or pipelines.
   - **Add Pipeline Model File** — a custom model or supporting file, if required.

6. **Write the scoring logic.** In the editor, write the Python that ties everything together and returns the result. Use **Format Code** to tidy it and **Test Code** to run it against sample input before saving.

7. **Finish registration.** Optionally add starting examples for human-in-the-loop testing and notes under **Additional Information**, then click **Create**. The pipeline is saved as a **Draft** until promoted.

</Steps>

## Variables available in scoring logic

When you write scoring logic for a **chat pipeline**, several variables are provided automatically — you do not need to declare them.

| Variable | Type | What it holds |
|----------|------|---------------|
| `user_message` | `str` | The current message from the user. |
| `history` | `list[TypedDict[{'role': str, 'content': str}]]` | All previous messages, in standard OpenAI format. |
| `context` | your **Context Type** | Information carried over from earlier turns. |
| `cache` | `dict` | A store for intermediate, reusable objects so expensive work is not repeated. One cache per pipeline, shared across all executions. |

:::note[About the output]
The output of a chat pipeline is fixed as a dictionary — `{"output": string, "context": custom type}`. The `output` is the reply shown to the user; the `context` is whatever you want available on the next turn, typed by the **Context Type** from Step 4.
:::

## Testing your pipeline

Once a pipeline is created, validate its behaviour before relying on it. There are three ways to test, in increasing order of thoroughness.

<figure class="ggx-figure">

![Three escalating test levels: Quick Test, Interactive Test, and Bulk Simulation, in increasing order of thoroughness.](./pipeline-testing-levels.svg)

<figcaption>From a quick sanity check on one input to a full run over an entire dataset.</figcaption>
</figure>

### Quick Test — during development

A fast sanity check while you are still writing the logic; it runs the code without saving.

<Steps>

1. While creating or editing the pipeline, scroll to the **Code** section.
2. Click **Test Code** in the bottom-right corner of the editor.
3. Enter sample inputs and confirm the logic returns what you expect.

</Steps>

### Interactive Test — feedbacks after initial version is created 

Once saved, test the pipeline the way an end user would experience it.

<Steps>

1. Navigate to your saved pipeline.
2. Click **Run → Chat Session** in the top-right corner.
3. Enter sample messages to walk through the full conversation flow.
4. Confirm the outputs match the expected behaviour.

</Steps>

:::note[Chat Session is for chat-based pipelines]
**Chat Session** is available only for **chat-based** pipelines. For **free-flow** and **classification** pipelines, use **Test Code** instead — call the function with sample inputs to check the output.
:::

### Bulk Simulation — validation at scale before for approvals

A single input tells you the pipeline *works*; a **bulk simulation** tells you how it behaves across many real cases. It runs every row of a dataset through the pipeline, producing one output per record. Use it to:

- Spot edge cases and inconsistent outputs a single test would miss.
- Measure quality across a representative dataset before promoting.
- Attach the run as evidence in the pipeline's **Risk Assessment** tab.

:::tip[When to use which]
Reach for **Quick Test** while writing the logic, **Interactive Test** to feel the end-user experience, and a **Bulk Simulation** before promoting to production — the most thorough check of the three.
:::

## A complete example: a card replacement assistant

This example fills in every field for a realistic **chat-based pipeline** that helps customers replace a lost card.

<details class="ggx-details">
<summary>Page fields for <code>card_assistant</code></summary>

| Field | Value |
|-------|-------|
| Description | *"Conversational assistant that helps a customer report a lost card and request a replacement. Use for card-servicing chats; not for fraud disputes."* |
| Alias | `card_assistant` |
| Input Type | Python Function |
| Pipeline Type | Chat Based Pipeline |
| Context Type | `dict[str, str]` |
| Resources | `kb` (a RAG over the card-policy knowledge base), `reply_prompt` (a Prompt), `chat_model` (an LLM) |

</details>

<Tabs>
<TabItem label="Chat-Based scoring logic">

```python title="card_assistant — scoring logic"
# Retrieve relevant card-policy passages for the user's message
docs = kb.search(user_message, top_k=3)  # (1)!

# Fill the prompt with the retrieved policy and the conversation so far
filled_prompt = reply_prompt(
    user_message=user_message,
    history=history,
    policy_docs=docs,
)

# Generate the reply
reply = chat_model(filled_prompt)

# Track where we are in the flow so the next turn knows the
# customer has already confirmed the card was lost
updated_context = dict(context)
updated_context["stage"] = "replacement_offered"  # (2)!

return {"output": reply, "context": updated_context}  # (3)!
```

1. `kb`, `reply_prompt`, and `chat_model` are **Resources** added in Step 5. `user_message` and `history` are provided automatically.
2. On the next turn, `context["stage"]` is available again — so the pipeline knows not to ask *"did you lose your card?"* twice.
3. Chat pipelines **must** return this exact `{"output", "context"}` shape.

</TabItem>
<TabItem label="Free-Flow variant">

A **Free-Flow** pipeline is simpler — no history, no context, and you define the output shape. For example, scoring the urgency of a support ticket:

```python title="urgency_scorer — scoring logic"
# `ticket_text` is a Config argument defined via Add Config
filled_prompt = urgency_prompt(ticket=ticket_text)
score = chat_model(filled_prompt)

return {"urgency": score}
```

</TabItem>
<TabItem label="Classification variant">

A **Classification** pipeline returns one label from a set you predefine at registration. For example, routing an incoming support message to the right team:

```python title="support_router — scoring logic"
# Allowed labels are predefined when the pipeline is registered
filled_prompt = routing_prompt(message=user_message)
label = chat_model(filled_prompt)  # one of: billing, technical, general

return label
```

</TabItem>
</Tabs>

## Connecting an external agent

If a pipeline already runs in another environment, connect it to GGX instead of rebuilding it. On the New Pipeline page, set **Input Type** to **External Agent** and provide the agent's API connection.

For example, an agent built in **Vertex AI Agent Playbooks** can be connected through its API. Integrations for common providers — **Vertex AI Agent Playbooks, AgentForce, Microsoft Copilot Studio, Vapi AI**, and others — are configured in the Integration Module, and new providers can be added by extending the framework.

:::note
Once connected, an external agent is tracked, tested, and monitored exactly like a pipeline built from scratch.
:::

<LinkButton href={`${import.meta.env.BASE_URL}integrations/`} variant="secondary" icon="right-arrow" iconPlacement="end">Browse available integrations</LinkButton>

</helper-panel>

## Pipeline risk assessment

Each pipeline has a dedicated **Risk Assessment** tab for documenting its assumptions, risks, and mitigations. Risks are recorded across several dimensions, and you can attach simulations as evidence of the testing performed.

These are example dimensions — the set is configurable and can be auto-detected from a pipeline's configuration:

| Dimension | What it captures |
|-----------|------------------|
| **Accuracy** | How reliably the pipeline produces correct results. |
| **Stability** | How consistently it behaves across inputs and over time. |
| **Ethics** | Fairness, bias, and responsible-use considerations. |
| **Vulnerability** | Exposure to misuse, adversarial input, or failure modes. |

## Capabilities unlocked by registration

Registering a pipeline — rather than running a loose script — is what turns it into a governed, reusable asset:

| Capability | What you get |
|------------|--------------|
| **Change tracking** | Automatic recording of modifications, with efficient version upgrades. |
| **Purpose enforcement** | Automatic detection of Permissible Purpose violations. |
| **Testing & comparison** | Evaluate against other pipelines using custom and standardized validation kits. |
| **Reusability** | Reuse across downstream applications, with visibility through Lineage Tracking. |
| **Auditable path to production** | A transparent, fully auditable journey with easier production monitoring. |
| **Human Integrated Testing** | Feedback logging and human-in-the-loop testing for chat-based pipelines. |
| **Executable artifacts** | Extract ready-to-productionize artifacts straight from the Registry. |
| **Better collaboration** | A shared base for continuous development and testing. |