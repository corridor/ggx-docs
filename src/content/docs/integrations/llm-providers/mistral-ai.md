---
title: "Mistral AI"
description: "Connect Mistral AI to GGX with an API key and use its models in prompts, agents, and evaluations."
---

[Mistral AI](https://mistral.ai/): Mistral AI provides the Mistral family of models through its own API. In GGX, Mistral AI is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers Mistral AI as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](../../../register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the key to model code as environment variables, so scoring logic can call Mistral AI without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Mistral AI card.
3. Enter your Mistral AI API key.
4. Save the connection.

GGX provides the key as `MISTRAL_API_KEY` in model code. The Mistral AI API is OpenAI-compatible, so scoring logic can use the OpenAI client with the base URL `https://api.mistral.ai/v1`.

Keys are write-only and stored encrypted.
