---
title: "Cloudflare AI Gateway"
description: "Register Cloudflare AI Gateway as a GGX Model Registry model and route GGX requests to providers available through your Cloudflare gateway."
---

[Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) provides visibility and control for AI applications, including analytics, logging, caching, rate limiting, retries, and model fallback. Cloudflare supports provider-specific endpoints that preserve the provider API schema while adding AI Gateway features.

In GGX, Cloudflare AI Gateway can be registered in the [Model Registry](../../register-and-refine/inventory-management/model-catalog/) as a Model. The registered GGX Model calls the Cloudflare gateway endpoint, and Cloudflare can connect to any provider or model that your gateway configuration and account permissions allow.

## When to use this integration

Use Cloudflare AI Gateway with GGX when:

- Cloudflare is the control plane for AI traffic observability, caching, rate limiting, retries, or fallback.
- Your production application already routes provider traffic through Cloudflare AI Gateway.
- You want GGX evaluations to test the same gateway path used in production.
- You want Cloudflare to handle runtime controls while GGX handles inventory, simulations, approvals, compliance evidence, and monitoring workflows.

## Register Cloudflare AI Gateway in the Model Registry

| GGX setting | Recommended value |
| --- | --- |
| **Name** | `cloudflare_gateway_<provider_or_model>` |
| **Description** | Identify the Cloudflare account, gateway ID, provider endpoint, model alias, and runtime controls such as caching, rate limits, retries, or fallback. |
| **Model Provider** | Use a custom/API-based model or Python function that calls the Cloudflare AI Gateway endpoint. |
| **Arguments** | `messages`, `model`, `temperature`, `max_tokens` |
| **Environment variables** | `CLOUDFLARE_AI_GATEWAY_BASE_URL`, `CLOUDFLARE_AI_GATEWAY_API_KEY`, `CLOUDFLARE_AI_GATEWAY_MODEL` |

Cloudflare provider-specific endpoints use this pattern:

```txt
https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/{provider}
```

For OpenAI-compatible providers, configure `CLOUDFLARE_AI_GATEWAY_BASE_URL` to the provider-specific Cloudflare endpoint for your account and gateway.

## Example scoring logic

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("CLOUDFLARE_AI_GATEWAY_API_KEY"),
    base_url=os.getenv("CLOUDFLARE_AI_GATEWAY_BASE_URL"),
)

selected_model = model if model else os.getenv("CLOUDFLARE_AI_GATEWAY_MODEL")

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

- Register separate GGX Models when Cloudflare routes to different providers or when each provider requires separate review.
- Document Cloudflare caching, retry, rate-limit, and fallback settings in the GGX Model Risk Assessment.
- If Cloudflare fallback is enabled, include route metadata in GGX output or monitoring data when available.
- Use GGX monitoring to evaluate production behavior after Cloudflare has applied runtime controls.

References:

- [Cloudflare AI Gateway overview](https://developers.cloudflare.com/ai-gateway/)
- [Cloudflare AI Gateway get started](https://developers.cloudflare.com/ai-gateway/get-started/)
