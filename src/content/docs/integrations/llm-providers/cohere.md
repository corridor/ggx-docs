---
title: "Cohere"
description: "Connect Cohere to GGX with an API key and use its models in prompts, agents, and evaluations."
---

[Cohere](https://cohere.com/): Cohere provides language models for enterprise use, with an OpenAI-compatible endpoint. In GGX, Cohere is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers Cohere as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](../../../register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the key to model code as environment variables, so scoring logic can call Cohere without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Cohere card.
3. Enter your Cohere API key.
4. Save the connection.

GGX provides the key as `COHERE_API_KEY` in model code. The Cohere API is OpenAI-compatible, so scoring logic can use the OpenAI client with the base URL `https://api.cohere.ai/compatibility/v1`.

Keys are write-only and stored encrypted.
