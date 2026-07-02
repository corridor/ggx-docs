---
title: "LiteLLM Gateway"
description: "Register LiteLLM as a GGX Model Registry model and route GGX requests to any LLM provider configured behind LiteLLM."
---

[LiteLLM](https://docs.litellm.ai/docs/) provides a unified interface for many LLM providers and includes a self-hosted proxy server that can expose an OpenAI-compatible gateway. LiteLLM is commonly used to standardize provider APIs, manage virtual keys, track spend, configure fallbacks, and route requests across model deployments.

In GGX, LiteLLM can be registered in the [Model Registry](../../register-and-refine/inventory-management/model-catalog/) as a Model. The registered GGX Model calls your LiteLLM proxy, and LiteLLM can route the request to any underlying LLM that your LiteLLM configuration exposes.

## When to use this integration

Use LiteLLM with GGX when:

- Your engineering team already uses LiteLLM as the LLM proxy.
- You want GGX pipelines to call the same model aliases that production applications call.
- You want to evaluate several providers through one gateway layer.
- You want LiteLLM to handle provider credentials, routing, fallback, or cost tracking while GGX handles evaluation, approval, and monitoring.

## Register LiteLLM in the Model Registry

Create one GGX Model per LiteLLM model alias, or create one parameterized model that accepts a `model` argument.

| GGX setting | Recommended value |
| --- | --- |
| **Name** | `litellm_<model_alias>` or `litellm_gateway` |
| **Description** | Note the LiteLLM proxy URL, allowed model aliases, provider list, and fallback policy. |
| **Model Provider** | Use a custom/API-based model or Python function that calls the LiteLLM proxy. |
| **Arguments** | `messages`, `model`, `temperature`, `max_tokens` |
| **Environment variables** | `LITELLM_API_KEY`, `LITELLM_BASE_URL`, `LITELLM_MODEL` |

## Example scoring logic

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("LITELLM_API_KEY"),
    base_url=os.getenv("LITELLM_BASE_URL"),
)

selected_model = model if model else os.getenv("LITELLM_MODEL")

completion = client.chat.completions.create(
    model=selected_model,
    messages=messages,
    temperature=float(temperature),
    max_tokens=int(max_tokens),
)

return {
    "output": completion.choices[0].message.content,
    "model": selected_model,
}
```

## Governance notes

- Register each approved LiteLLM model alias as a separate GGX Model if business or risk reviewers need model-level approval.
- Document whether LiteLLM fallback is enabled, because fallback may cause a single GGX Model to use more than one underlying provider.
- Include LiteLLM request IDs, selected model names, or provider metadata in GGX outputs when available, so evaluation and monitoring dashboards can segment results by actual route.

Reference: [LiteLLM documentation](https://docs.litellm.ai/docs/)
