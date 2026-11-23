---
title: "GitHub Models"
description: "Connect GitHub Models to GGX with an API key and route model calls through it."
---

[GitHub Models](https://github.com/marketplace/models): GitHub Models lets you call models from the GitHub catalog with a GitHub token. In GGX, it is an LLM gateway: models registered in GGX can call it, and it routes to the models it has access to. See [LLM Gateways](../) for the general pattern.

## What it does in GGX

- Registers GitHub Models under **LLM Gateways** in **Org Settings → Integrations**.
- Exposes the credentials to model code as environment variables, so models registered in [Models](../../../register-and-refine/inventory-management/model-catalog/) can call the gateway without embedding secrets.
- Models served through the gateway take part in GGX simulations, comparisons, approvals, and monitoring.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Gateways** group.
2. Click the GitHub Models card.
3. Enter your GitHub Models token.
4. Save the connection.

GGX provides `GITHUB_TOKEN` in model code. Secrets are write-only and stored encrypted.

## Notes

A gateway can serve a different model than the one you ask for (fallbacks, aliases, routing). Record what sits behind the gateway in the model description and risk assessment.
