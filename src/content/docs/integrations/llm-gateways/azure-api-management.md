---
title: "Azure API Management"
description: "Connect Azure API Management to GGX with its base URL and credentials and route model calls through it."
---

[Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities): Azure API Management is Microsoft's API gateway; its AI gateway capabilities front LLM backends from your own instance. In GGX, it is an LLM gateway: models registered in GGX can call it, and it routes to the models it has access to. See [LLM Gateways](../) for the general pattern.

## What it does in GGX

- Registers Azure API Management under **LLM Gateways** in **Org Settings → Integrations**.
- Exposes the credentials to model code as environment variables, so models registered in [Models](../../../register-and-refine/inventory-management/model-catalog/) can call the gateway without embedding secrets.
- Models served through the gateway take part in GGX simulations, comparisons, approvals, and monitoring.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Gateways** group.
2. Click the Azure API Management card.
3. Enter the base URL of your gateway (for example `https://<instance>.azure-api.net/llm/v1`) and your subscription key.
4. Save the connection.

The gateway runs in your own environment, so its address must be reachable from the GGX API.

GGX provides `AZURE_APIM_SUBSCRIPTION_KEY` and `AZURE_APIM_BASE_URL` in model code. Secrets are write-only and stored encrypted.

## Notes

A gateway can serve a different model than the one you ask for (fallbacks, aliases, routing). Record what sits behind the gateway in the model description and risk assessment.

## GenGuardX on Microsoft Marketplace

GenGuardX is listed on [Microsoft Marketplace](https://marketplace.microsoft.com/en-us/product/corridorplatforms.corridorggx).
