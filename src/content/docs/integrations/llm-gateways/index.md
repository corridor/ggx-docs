---
title: "LLM Gateways"
description: "Use LLM gateways with GGX by registering gateway-backed models in the Model Registry and routing requests to any LLM the gateway can access."
---

LLM gateways provide a common API layer in front of one or more model providers. They are useful when your organization already centralizes routing, provider credentials, cost controls, logging, rate limits, caching, fallback, or provider selection outside GGX.

In GGX, an LLM gateway can be registered in the [Model Registry](../../register-and-refine/inventory-management/model-catalog/) as a Model. Once registered, that model can be used in prompts, RAGs, pipelines, simulations, comparisons, approval workflows, and production monitoring just like any directly integrated LLM provider.

## How the pattern works

1. Configure the LLM gateway with the providers and model aliases it is allowed to access.
2. Store the gateway base URL, API key, and default model alias in GGX environment variables or integration settings.
3. Register a GGX Model that calls the gateway endpoint.
4. Use the registered GGX Model in pipelines and evaluations.
5. Let the gateway route to any underlying LLM it has access to, while GGX records governance metadata, test evidence, approvals, lineage, and monitoring results.

## Registration options

| Option | When to use it |
| --- | --- |
| **One GGX Model per gateway model alias** | Use this when reviewers should approve and monitor each underlying LLM separately. For example, register `gateway_gpt4o`, `gateway_claude_sonnet`, and `gateway_gemini_flash` as separate GGX Models. |
| **One parameterized GGX Model** | Use this when the gateway chooses the model dynamically or when the caller should pass a `model` argument. This is useful for routing tests, fallback tests, and cost or latency comparisons. |
| **Gateway-backed pipeline** | Use this when the gateway is only one component in a larger GGX Pipeline that also includes prompts, retrieval, guardrails, parsing, or business logic. |

## Model Registry setup

When registering an LLM gateway in the Model Registry, capture enough metadata for business, risk, and audit reviewers to understand what is behind the gateway.

| Field | Recommended value |
| --- | --- |
| **Name** | A clear name such as `litellm_gateway_gpt4o`, `portkey_gateway_default`, or `cloudflare_gateway_openai`. |
| **Description** | State that the GGX Model calls an LLM gateway and identify the gateway, allowed providers, model aliases, and routing policy. |
| **Input Type** | Use an API-based or Python-function model implementation, depending on how the gateway is reached in your environment. |
| **Arguments** | Include `messages`, `prompt`, `model`, `temperature`, `max_tokens`, and any request tags your gateway supports. |
| **Output Type** | Use `String` for simple responses or `Map[String, String]` when returning response text plus metadata such as selected model, gateway request ID, or routing outcome. |
| **Risk Assessment** | Document the gateway owner, approved provider list, fallback policy, logging policy, data retention behavior, and whether prompts or responses are stored by the gateway. |

## Generic OpenAI-compatible example

Many gateways expose an OpenAI-compatible API. Register a GGX Model with scoring logic like this, then set the environment variables for the gateway you use.

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("LLM_GATEWAY_API_KEY"),
    base_url=os.getenv("LLM_GATEWAY_BASE_URL"),
)

selected_model = model if model else os.getenv("LLM_GATEWAY_MODEL")

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

## Gateway-specific guides

- [LiteLLM](litellm/)
- [Portkey](portkey/)
- [OpenRouter](openrouter/)
- [Cloudflare AI Gateway](cloudflare-ai-gateway/)

## What GGX adds on top of an LLM gateway

LLM gateways centralize runtime access. GGX adds lifecycle governance around the AI system that uses that gateway:

- Model Registry inventory, ownership, and descriptions.
- Version history and lineage for prompts, models, RAGs, pipelines, reports, and data.
- Automated simulations and comparisons across gateway-backed models.
- Standardized risk reports for accuracy, stability, bias, toxicity, vulnerability, hallucination, retrieval quality, and other compliance dimensions.
- Approval workflows for business, risk, legal, compliance, technology, and model-risk reviewers.
- Production monitoring, dashboards, alerts, and annotation queues.
