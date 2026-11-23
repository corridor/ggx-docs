---
title: "Apache APISIX Gateway"
description: "Register Apache APISIX as a GGX Model and route GGX requests through the AI plugins of your APISIX gateway."
---

[Apache APISIX](https://apisix.apache.org/) is an open-source API gateway. Its AI plugins, such as `ai-proxy`, put an OpenAI-style chat endpoint on a Route and forward requests to the LLM provider you configure. APISIX is self-hosted, so your team owns the Route and its authentication.

In GGX, APISIX can be registered on the [Models](../../../register-and-refine/inventory-management/model-catalog/) page as a Model. The registered Model calls your APISIX Route.

## Connect APISIX in GGX

1. Open **Org Settings → Integrations** from the profile menu, and find **Apache APISIX** under **LLM Gateways**.
2. Click **Configure**, then enter the **API Endpoint** and the **API Key**.
3. Save.

The endpoint is available to model code as `APISIX_BASE_URL` and the key as `APISIX_API_KEY`. GGX has no connection test for APISIX, so check the Route with a registered Model.

A project can use its own endpoint and key instead of the organization's.

### What to enter

- **API Endpoint**: the full URL of your Route, such as `http://apisix:9080/v1/chat`. APISIX has no fixed path: the path is the `uri` of the Route your administrator created.
- **API Key**: the key of an APISIX consumer. APISIX reads it from the `apikey` header when the Route uses the `key-auth` plugin, not from the `Authorization` header.

## Register APISIX as a Model

| GGX setting | Recommended value |
| --- | --- |
| **Name** | `apisix_<route>` or `apisix_gateway` |
| **Description** | Note the Route, the provider behind it, and any rate limiting or fallback your APISIX applies. |
| **Model Provider** | Use a custom/API-based model or Python function that calls the Route. |
| **Arguments** | `messages`, `model`, `temperature`, `max_tokens` |
| **Environment variables** | `APISIX_API_KEY` and `APISIX_BASE_URL`, set by the integration |

## Example scoring logic

```python
import os
from openai import OpenAI

# APISIX reads the key from the apikey header (key-auth), not from Authorization
client = OpenAI(
    base_url=os.environ["APISIX_BASE_URL"],
    api_key="unused",
    default_headers={"apikey": os.environ["APISIX_API_KEY"]},
)

completion = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=float(temperature),
    max_tokens=int(max_tokens),
)

return {"output": completion.choices[0].message.content}
```

If your Route uses another authentication plugin, change the header in `default_headers` to match it.

## Governance notes

- The model behind a Route is set in the APISIX plugin configuration. Name it in the GGX Model's description so reviewers know what they are approving.
- Ask your APISIX administrator whether the Route honors the `model` and sampling parameters you send. A Route that ignores them can make a comparison misleading.
- If APISIX rate limiting is on, a rejected request may return status 503 or 429, depending on how the administrator configured it. Treat both as retryable.

Reference: [APISIX ai-proxy plugin](https://apisix.apache.org/docs/apisix/plugins/ai-proxy/)
