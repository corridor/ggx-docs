---
title: "Kong AI Gateway"
description: "Connect Kong AI Gateway to GGX with its base URL and credentials and route model calls through it."
---

[Kong AI Gateway](https://developer.konghq.com/ai-gateway/): Kong AI Gateway is run by your organization and routes requests to LLM providers. In GGX, it is an LLM gateway: models registered in GGX can call it, and it routes to the models it has access to. See [LLM Gateways](../) for the general pattern.

## What it does in GGX

- Registers Kong AI Gateway under **LLM Gateways** in **Org Settings → Integrations**.
- Exposes the credentials to model code as environment variables, so models registered in [Models](../../../register-and-refine/inventory-management/model-catalog/) can call the gateway without embedding secrets.
- Models served through the gateway take part in GGX simulations, comparisons, approvals, and monitoring.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Gateways** group.
2. Click the Kong AI Gateway card.
3. Enter the base URL of your gateway (for example `https://kong.example.com/v1`) and your API key.
4. Save the connection.

The gateway runs in your own environment, so its address must be reachable from the GGX API.

GGX provides `KONG_AI_API_KEY` and `KONG_AI_BASE_URL` in model code. Secrets are write-only and stored encrypted.

## Notes

A gateway can serve a different model than the one you ask for (fallbacks, aliases, routing). Record what sits behind the gateway in the model description and risk assessment.
