# Global Functions
Source: https://docs.genguardx.ai/register-and-refine/inventory-management/global-functions/
Markdown: https://docs.genguardx.ai/register-and-refine/inventory-management/global-functions/index.md
Description: How Global Functions work in GGX — reusable analytical logic with inputs and outputs of any type, registered once and called across pipelines, RAGs, models, reports, and simulations.
<helper-panel object='Global Function' location='list'>

## What is a Global Function?

A **Global Function** lets you write a set of analytical operations **once** and run them many times with different objects as inputs — without rewriting the logic each time. It supports inputs and outputs of **any type** (DataFrames, dictionaries, plain Python values, and more) and does **not** require a predefined input/output schema.

Because it is registered centrally, the same function can be called across the platform — inside GenAI Studio, Reports, Simulation Data Sources, or even other Global Functions — which is what makes it the platform's primary unit of reuse.

<figure class="ggx-figure">

![Global Function anatomy: inputs of any type flow into reusable logic that returns an output of any type, and the same function is reused across GenAI Studio, Reports, Simulation Data Sources, and other Global Functions.](./global-function-concept.svg)

<figcaption>Write the logic once; call it with different inputs from anywhere on the platform.</figcaption>
</figure>

## A worked example: masking card numbers

Consider `mask_card`, a small utility that redacts card numbers in free text — keeping only the last four digits. It is the kind of operation many objects need: the [card-replacement assistant](../pipelines/#a-complete-example-a-card-replacement-assistant) calls it before logging a conversation, a RAG calls it to sanitise retrieved passages, and a compliance Report calls it on its output. Register it once, and all three reuse the same audited logic.

## Anatomy of a Global Function

| Part | What it holds | Required? |
|------|---------------|-----------|
| **Definition / code** | The Python that performs the operation and returns a result. | <Badge text="required" variant="caution" /> |
| **Input Arguments** | Each input the logic operates on, with its **Alias**, **Type**, optional flag, and default value. | Optional |
| **Output Type** | The data type the function returns. | Optional — see note below |
| **Resources** | Other registered Global Functions the logic can call. | Optional |
| **Properties** | Description, Group, Approval Workflow. | Mostly required |
| **Attributes** | <Badge text="Alias" variant="caution" /> — the Python variable name other objects call this function by. | <Badge text="required" variant="caution" /> |

:::note[Output type is optional]
Unlike most registered objects, a Global Function does **not** require an Output Type. If you leave it unset, the function may return **any** type — a DataFrame, a dictionary, a tuple, and so on.
:::

## Where Global Functions are used

Once registered, a Global Function is available anywhere logic runs on the platform:

<CardGrid>
<Card title="GenAI Studio" icon="puzzle">
Call it from a **Pipeline**, **Model**, or **RAG** as a registered Resource — shared pre/post-processing, formatting, or scoring helpers.
</Card>
<Card title="Reports" icon="document">
Reuse the same logic when writing **Reports**, so report calculations match what runs in production.
</Card>
<Card title="Simulation Data Sources" icon="random">
Prepare or transform the data that feeds a **bulk simulation**.
</Card>
<Card title="Other Global Functions" icon="list-format">
Compose functions — a Global Function can call other registered Global Functions.
</Card>
</CardGrid>

## Adding a Global Function to the registry

The **Global Function Registry** is the central place where every registered utility lives, organised into customisable groups for easier tracking, monitoring, and creation.

Click **Create** on the registry page, then work through the form:

<Steps>

1. **Name, Properties, and Attributes.** Give the function a clear name and description. Set the **Group** and **Approval Workflow** under Properties, and the **Output Type** (optional) and <Badge text="Alias" variant="caution" /> under Attributes.

2. **Input Arguments.** Define each argument with its **Alias**, **Type**, optional flag, and default value.

3. **Resources.** Select any other registered Global Functions the logic should be able to call.

4. **Definition source.** Write the Python that performs the operation and returns the result. Use **Test Code** to run it against sample inputs before saving.

5. **Additional Information.** Add notes or attach supporting documentation.

6. **Save.** Click **Save** to register. The function is saved as a **Draft** until it goes through approval.

</Steps>

## A complete example: `mask_card`

This fills in every field for the `mask_card` utility introduced above.

<details class="ggx-details">
<summary>Page fields for <code>mask_card</code></summary>

| Field | Value |
|-------|-------|
| Description | *"Redacts card numbers in free text, keeping only the last four digits. Reusable across pipelines, RAGs, and reports for safe logging and display."* |
| Alias | `mask_card` |
| Output Type | `str` |
| Input Arguments | `text` (`str`, required) |
| Resources | — |

</details>

<Tabs>
<TabItem label="Definition">

```python title="mask_card — definition source"
import re

# Replace any 13–16 digit sequence with •••• and its last four digits
def _mask(match):
    digits = re.sub(r"\D", "", match.group())
    return "•••• " + digits[-4:]

return re.sub(r"\b(?:\d[ -]?){13,16}\b", _mask, text)
```

:::note
`text` is the Input Argument defined in Step 2, and the return value matches the declared **Output Type** `str`.
:::

</TabItem>
<TabItem label="Calling it">

Once registered, call it by its **Alias** from any pipeline, RAG, model, or report:

```python
# inside a pipeline's scoring logic, before logging the turn
safe_message = mask_card(user_message)
```

</TabItem>
</Tabs>

</helper-panel>

## Testing a Global Function

While writing the definition, click **Test Code** at the bottom of the editor to run the function against sample inputs without saving — confirm it returns what you expect and that the return value matches the declared **Output Type** (if you set one). Because functions are composed into other objects, they also get exercised end-to-end whenever a pipeline, RAG, or report that uses them is run or simulated.

## Capabilities unlocked by registration

Registering a Global Function — rather than copy-pasting a helper into every script — is what turns it into a governed, reusable asset:

| Capability | What you get |
|------------|--------------|
| **Reusability** | Call the same logic across pipelines, models, RAGs, reports, and simulations, with visibility through [Lineage Tracking](../../lineage-tracking/). |
| **Change tracking** | Automatic recording of modifications with efficient version upgrades. |
| **Auditable path to production** | A transparent, fully auditable journey from Draft through Approval to downstream use. |
| **Better collaboration** | A shared base for continuous building and testing across teams. |