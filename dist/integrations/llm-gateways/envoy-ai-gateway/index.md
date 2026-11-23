# Envoy AI Gateway (Agent Router)
Source: https://docs.genguardx.ai/integrations/llm-gateways/envoy-ai-gateway/
Markdown: https://docs.genguardx.ai/integrations/llm-gateways/envoy-ai-gateway/index.md
Description: Connect Envoy AI Gateway (Agent Router) to GGX with its base URL and credentials and route model calls through it.

[Envoy AI Gateway (Agent Router)](https://github.com/envoyproxy/ai-gateway): Envoy AI Gateway is an open-source gateway that your organization runs to route requests to LLM providers. In GGX, it is an LLM gateway: models registered in GGX can call it, and it routes to the models it has access to. See [LLM Gateways](https://docs.genguardx.ai/integrations/llm-gateways/) for the general pattern.

## What it does in GGX

- Registers Envoy AI Gateway (Agent Router) under **LLM Gateways** in **Org Settings → Integrations**.
- Exposes the credentials to model code as environment variables, so models registered in [Models](https://docs.genguardx.ai/register-and-refine/inventory-management/model-catalog/) can call the gateway without embedding secrets.
- Models served through the gateway take part in GGX simulations, comparisons, approvals, and monitoring.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Gateways** group.
2. Click the Envoy AI Gateway (Agent Router) card.
3. Enter the base URL of your gateway (for example `https://envoy.example.com/v1`) and your API key. The key is optional if the gateway holds the provider credentials itself.
4. Save the connection.

The gateway runs in your own environment, so its address must be reachable from the GGX API.

GGX provides `ENVOY_AI_API_KEY` and `ENVOY_AI_BASE_URL` in model code. Secrets are write-only and stored encrypted.

## Notes

A gateway can serve a different model than the one you ask for (fallbacks, aliases, routing). Record what sits behind the gateway in the model description and risk assessment.
