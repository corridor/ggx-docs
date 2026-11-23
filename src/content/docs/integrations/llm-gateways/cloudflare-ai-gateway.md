---
title: "Cloudflare AI Gateway"
description: "Register Cloudflare AI Gateway as a GGX Model and route GGX requests to providers available through your Cloudflare gateway."
---

[Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/) provides visibility and control for AI applications, including analytics, logging, caching, rate limiting, retries, and model fallback. Cloudflare supports provider-specific endpoints that preserve the provider API schema while adding AI Gateway features.

In GGX, Cloudflare AI Gateway can be registered on the [Models](../../../register-and-refine/inventory-management/model-catalog/) page as a Model. The registered GGX Model calls the Cloudflare gateway endpoint, and Cloudflare can connect to any provider or model that your gateway configuration and account permissions allow.

## When to use this integration

Use Cloudflare AI Gateway with GGX when:

- Cloudflare is the control plane for AI traffic observability, caching, rate limiting, retries, or fallback.
- Your production application already routes provider traffic through Cloudflare AI Gateway.
- You want GGX evaluations to test the same gateway path used in production.
- You want Cloudflare to handle runtime controls while GGX handles inventory, simulations, approvals, compliance evidence, and monitoring workflows.

## Connect Cloudflare AI Gateway in GGX

1. Open **Org Settings → Integrations** from the profile menu, and find **Cloudflare AI Gateway** under **LLM Gateways**.
2. Click **Configure** and enter:
    - **Account ID** and **Gateway ID** of your Cloudflare AI Gateway;
    - **Gateway token**, if the gateway is authenticated;
    - **API Key** (optional), the key of the upstream provider if Cloudflare does not hold it.
3. Click **Save**.

The integration sets these environment variables for model code:

| Field | Environment variable |
| --- | --- |
| Account ID | `CLOUDFLARE_ACCOUNT_ID` |
| Gateway ID | `CLOUDFLARE_GATEWAY_ID` |
| Gateway token | `CF_AIG_TOKEN` |
| API Key | `CLOUDFLARE_AI_GATEWAY_API_KEY` |

## Register Cloudflare AI Gateway as a Model

| GGX setting | Recommended value |
| --- | --- |
| **Name** | `cloudflare_gateway_<provider_or_model>` |
| **Description** | Identify the Cloudflare account, gateway ID, provider endpoint, model alias, and runtime controls such as caching, rate limits, retries, or fallback. |
| **Model Provider** | Use a custom/API-based model or Python function that calls the Cloudflare AI Gateway endpoint. |
| **Arguments** | `messages`, `model`, `temperature`, `max_tokens` |
| **Environment variables** | `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_GATEWAY_ID`, `CF_AIG_TOKEN` and `CLOUDFLARE_AI_GATEWAY_API_KEY` (set by the integration), and optionally your own `CLOUDFLARE_AI_GATEWAY_MODEL` default |

Cloudflare provider-specific endpoints use this pattern:

```txt
https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/{provider}
```

Build the endpoint in your scoring logic from `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_GATEWAY_ID`, using the provider segment of the upstream provider (for example `openai`).

## Example scoring logic

```python
import os
from openai import OpenAI

account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
gateway_id = os.getenv("CLOUDFLARE_GATEWAY_ID")
gateway_token = os.getenv("CF_AIG_TOKEN")

client = OpenAI(
    api_key=os.getenv("CLOUDFLARE_AI_GATEWAY_API_KEY"),
    base_url=f"https://gateway.ai.cloudflare.com/v1/{account_id}/{gateway_id}/openai",
    default_headers={"cf-aig-authorization": f"Bearer {gateway_token}"} if gateway_token else None,
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
