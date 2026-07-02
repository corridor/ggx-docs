---
title: "OpenRouter Gateway"
description: "Register OpenRouter as a GGX Model Registry model and route GGX requests to OpenRouter-supported models through a unified API."
---

[OpenRouter](https://openrouter.ai/docs/quickstart) provides a unified API for accessing many AI models through a single endpoint. It supports direct API calls and OpenAI-compatible SDK usage, so GGX can call OpenRouter as a gateway-backed model.

In GGX, OpenRouter can be registered in the [Model Registry](../../register-and-refine/inventory-management/model-catalog/) as a Model. The registered GGX Model calls OpenRouter, and OpenRouter can route to any model that your OpenRouter account and request configuration can access.

## When to use this integration

Use OpenRouter with GGX when:

- You want a single model-access endpoint for many third-party models.
- You want to compare models available through OpenRouter using GGX simulations and comparison jobs.
- You want GGX pipelines to use OpenRouter model slugs instead of provider-specific SDKs.
- You need quick access to multiple hosted models while keeping GGX as the governance and approval layer.

## Register OpenRouter in the Model Registry

| GGX setting | Recommended value |
| --- | --- |
| **Name** | `openrouter_<model_slug>` or `openrouter_gateway` |
| **Description** | Identify the OpenRouter model slug, routing preferences, and whether fallback or model aliases are used. |
| **Model Provider** | Use a custom/API-based model or Python function that calls OpenRouter. |
| **Arguments** | `messages`, `model`, `temperature`, `max_tokens` |
| **Environment variables** | `OPENROUTER_API_KEY`, `OPENROUTER_MODEL` |

## Example scoring logic

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

selected_model = model if model else os.getenv("OPENROUTER_MODEL")

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

- Register one GGX Model per OpenRouter model slug when each model needs separate approval evidence.
- Use GGX comparison jobs to evaluate challenger OpenRouter models against the same dataset and reports.
- Record the OpenRouter model slug in the GGX Model description and exported evidence.
- If you use OpenRouter aliases or routing controls, document them in the GGX Risk Assessment so reviewers understand what model may answer a request.

Reference: [OpenRouter quickstart](https://openrouter.ai/docs/quickstart)
