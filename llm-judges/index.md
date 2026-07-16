# LLM Judges
Source: https://docs.genguardx.ai/llm-judges/
Markdown: https://docs.genguardx.ai/llm-judges/index.md
Description: A gallery of ready-to-use LLM-as-a-Judge evaluators for GenGuardX. Browse by category and inspect each judge's prompt and code.
## What is an LLM Judge?

An **LLM-as-a-Judge** uses a large language model to evaluate the output of
another AI system — scoring qualities that are hard to measure with rules or
exact-match metrics, such as answer relevancy, factual accuracy, coherence,
toxicity, or bias. Instead of asking a human reviewer to grade every response, a
judge is given a rubric (the **prompt**) and returns a structured verdict — a
score and a short reasoning — that you can aggregate, monitor, and act on at
scale.

Every judge in this catalog is a ready-to-use GenGuardX component. It pairs a
carefully written evaluation **prompt** with a `Judge Model` that is
model-agnostic (it connects through **AnyLLM**, so you can point it at OpenAI,
Gemini, Anthropic, Bedrock, and more) and validates its output against a
**pydantic** model, so you always get well-formed, typed results. Search or
filter by category below, then open any card to inspect its prompt and code.

## Syncing a judge to your instance

Each judge ships as a self-contained Python file that declares its prompt and
model with GGX decorators and syncs them with `ggx.sync`. To add a judge to your
GenGuardX instance:

<Steps>

1. **Install the SDK** and open the judge you want from the catalog below.

   ```bash
   pip install genguardx
   ```

2. **Copy the judge's code** into a file in your project (e.g. `judge.py`). Use
   the **Code** tab on any card to grab the full source.

3. **Set your credentials.** The judges read them from the environment — put your
   instance URL and [API key](/register-and-refine/sync/#obtaining-your-api-key)
   in a `.env` file:

   ```bash
   GGX_API_URL="https://your-ggx-instance.example.com"
   GGX_API_KEY="your-api-key-here"
   ```

4. **Run the file to sync it.** The `__main__` block calls `ggx.init(...)` and
   `ggx.sync(...)`, registering the judge's prompt and model on your instance:

   ```bash
   python judge.py
   ```

</Steps>

Once synced, the judge appears in your inventory and can be used for downstream applications. See the full reference for details.

<LinkButton href={`${import.meta.env.BASE_URL}register-and-refine/sync/`} variant="secondary" icon="right-arrow">
  GGX Sync reference
</LinkButton>

:::caution[Test and adapt before you rely on a judge]
These judges are strong, general-purpose starting points — not drop-in ground
truth. LLM judges can be sensitive to your domain, data distribution, and
scoring conventions. Before you depend on one, **validate it on your specific
task and data** (ideally against a set of human-labeled examples) and **adapt
the prompt, scoring scale, or model as needed** to get reliable results.
:::

## Browse the catalog

<LlmJudges />