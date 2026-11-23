---
title: "LLM Gateways"
description: "Use LLM gateways with GGX by registering gateway-backed models under Data & AI Assets → Models and routing requests to any LLM the gateway can access."
---

LLM gateways provide a common API layer in front of one or more model providers. They are useful when your organization already centralizes routing, provider credentials, cost controls, logging, rate limits, caching, fallback, or provider selection outside GGX.

In GGX, an LLM gateway can be registered on the [Models](../../register-and-refine/inventory-management/model-catalog/) page as a Model. Once registered, that model can be used in prompts, RAGs, agents, simulations, comparisons, approval workflows, and production monitoring just like any directly integrated LLM provider.

## How the pattern works

1. Configure the LLM gateway with the providers and model aliases it is allowed to access.
2. Connect the gateway in **Org Settings → Integrations → LLM Gateways**. The integration stores the gateway's URL and credentials as environment variables for your model code. Gateways without their own entry can use **Other OpenAI-compatible gateway**.
3. Register a GGX Model that calls the gateway endpoint.
4. Use the registered GGX Model in agents and evaluations.
5. Let the gateway route to any underlying LLM it has access to, while GGX records governance metadata, test evidence, approvals, lineage, and monitoring results.

## Registration options

| Option | When to use it |
| --- | --- |
| **One GGX Model per gateway model alias** | Use this when reviewers should approve and monitor each underlying LLM separately. For example, register `gateway_gpt4o`, `gateway_claude_sonnet`, and `gateway_gemini_flash` as separate GGX Models. |
| **One parameterized GGX Model** | Use this when the gateway chooses the model dynamically or when the caller should pass a `model` argument. This is useful for routing tests, fallback tests, and cost or latency comparisons. |
| **Gateway-backed agent** | Use this when the gateway is only one component in a larger GGX Agent that also includes prompts, retrieval, guardrails, parsing, or business logic. |

## Model setup

When registering an LLM gateway as a Model, capture enough metadata for business, risk, and audit reviewers to understand what is behind the gateway.

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
- [Databricks AI Gateway](databricks-ai-gateway/)
- [NVIDIA NIM](nvidia-nim/)
- [GitHub Models](github-models/)
- [Helicone AI Gateway](helicone-ai-gateway/)
- [TrueFoundry AI Gateway](truefoundry-ai-gateway/)
- [Vercel AI Gateway](vercel-ai-gateway/)
- [Kong AI Gateway](kong-ai-gateway/)
- [Apache APISIX](apache-apisix/)
- [Envoy AI Gateway (Agent Router)](envoy-ai-gateway/)
- [Gloo AI Gateway](gloo-ai-gateway/)
- [Azure API Management](azure-api-management/)

## Other OpenAI-compatible gateways

If your gateway has no page above, connect it as an **Other OpenAI-compatible gateway**.

1. Open **Org Settings → Integrations → LLM Gateways**, find **Other OpenAI-compatible gateway**, and click **Add**.
2. Enter a **Name**. It shows in the integrations list and in the model picker.
3. Enter the **Base URL**: the full address of the OpenAI-compatible API, with any path, such as `https://gateway.example.com/v1`. A **Path prefix (optional)** is added to it.
4. Enter the **API key** and the **Header of the API key** your gateway reads. The key is optional: without it GGX sends no credential, which suits a gateway that holds the provider key or needs none. The **Scheme** is the word before the value, such as `Bearer`; use `none` to send the value alone. Use **Add another secret header** for more.
5. Optionally add **Extra headers** that are not secret, for example to route or to name a team. Credentials belong in the secret headers.
6. Optionally add **Body fields**: a JSON object merged into every request, for gateway options such as routing or caching. It cannot set the model, messages, stream, or tools.
7. For a gateway with a private certificate, paste its authority under **Custom CA certificate (optional)**. GGX checks it as well as the usual authorities and never turns verification off.
8. Add the models. Enter the **Model list path** (such as `/models`) and select **Fetch models**, or type the **Model names**, one per line, exactly as the gateway writes them. They appear in the model picker under the gateway's name.
9. Select **Test connection**, then save. A gateway that is not **Enabled** is not offered and not used.

## Gateways per project

Gateways are set up for the organization, and a project can adjust them in **Project Settings → Integrations**. A gateway of the organization shows as **Inherited**, or **Overridden** when the project has its own configuration of it. In the dialog, **Inherit from Org Settings** is on by default. Turn it off to give the project its own address and credentials: the project does not share the credentials of the organization, so enter the ones it needs. A project can also add a gateway the organization does not have. That gateway belongs to the project alone.

## What GGX adds on top of an LLM gateway

LLM gateways centralize runtime access. GGX adds lifecycle governance around the AI system that uses that gateway:

- Model inventory, ownership, and descriptions.
- Version history and lineage for prompts, models, RAGs, agents, reports, and data.
- Automated simulations and comparisons across gateway-backed models.
- Standardized risk reports for accuracy, stability, bias, toxicity, vulnerability, hallucination, retrieval quality, and other compliance dimensions.
- Approval workflows for business, risk, legal, compliance, technology, and model-risk reviewers.
- Production monitoring, dashboards, alerts, and annotation queues.
