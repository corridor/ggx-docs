---
title: "xAI"
description: "Connect xAI to GGX with an API key and use its models in prompts, agents, and evaluations."
---

[xAI](https://x.ai/): xAI provides the Grok models through an OpenAI-compatible API. In GGX, xAI is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers xAI as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](../../../register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the key to model code as environment variables, so scoring logic can call xAI without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the xAI card.
3. Enter your xAI API key.
4. Save the connection.

GGX provides the key as `XAI_API_KEY` in model code. The xAI API is OpenAI-compatible, so scoring logic can use the OpenAI client with the base URL `https://api.x.ai/v1`.

Keys are write-only and stored encrypted.
