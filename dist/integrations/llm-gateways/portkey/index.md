# Portkey Gateway
Source: https://docs.genguardx.ai/integrations/llm-gateways/portkey/
Markdown: https://docs.genguardx.ai/integrations/llm-gateways/portkey/index.md
Description: Register Portkey as a GGX Model Registry model and use Portkey provider routing with GGX evaluations, pipelines, approvals, and monitoring.
[Portkey](https://docs.portkey.ai/docs/introduction/what-is-portkey) is an AI gateway that provides a unified interface for many AI models, with tooling for visibility, routing, control, and security. Portkey can be used directly through its SDK or through OpenAI-compatible clients pointed at the Portkey gateway.

In GGX, Portkey can be registered in the [Model Registry](../../register-and-refine/inventory-management/model-catalog/) as a Model. The registered GGX Model calls Portkey, and Portkey can connect to any LLM provider or model that your Portkey configuration allows.

## When to use this integration

Use Portkey with GGX when:

- Portkey is the enterprise gateway for model access.
- Teams use Portkey provider configs, routing rules, or observability in production.
- You want GGX evaluation and approval evidence to exercise the same gateway route as production.
- You need GGX to test multiple Portkey-backed providers without adding each provider directly to GGX.

## Register Portkey in the Model Registry

| GGX setting | Recommended value |
| --- | --- |
| **Name** | `portkey_<provider_or_model>` or `portkey_gateway` |
| **Description** | Identify the Portkey provider, config, model alias, routing behavior, and any data logging policy. |
| **Model Provider** | Use a custom/API-based model or Python function that calls the Portkey gateway. |
| **Arguments** | `messages`, `model`, `temperature`, `max_tokens`, optional `provider` or config identifier |
| **Environment variables** | `PORTKEY_API_KEY`, `PORTKEY_BASE_URL`, `PORTKEY_PROVIDER`, `PORTKEY_MODEL` |

## Example scoring logic

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("PORTKEY_UPSTREAM_API_KEY", "not-used"),
    base_url=os.getenv("PORTKEY_BASE_URL"),
    default_headers={
        "x-portkey-api-key": os.getenv("PORTKEY_API_KEY"),
        "x-portkey-provider": provider if provider else os.getenv("PORTKEY_PROVIDER"),
    },
)

selected_model = model if model else os.getenv("PORTKEY_MODEL")

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

- Register separate GGX Models for Portkey providers or configs that require separate approvals.
- Capture the Portkey provider/config name in the GGX Model description and Risk Assessment.
- If Portkey routing can shift between upstream LLMs, include route metadata in GGX evaluation outputs whenever available.
- Use GGX simulations and comparisons to test whether Portkey routing changes affect accuracy, stability, safety, latency, or cost-sensitive behavior.

Reference: [Portkey documentation](https://docs.portkey.ai/docs/introduction/what-is-portkey)