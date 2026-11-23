---
title: "Fireworks AI"
description: "Connect Fireworks AI to GGX with an API key and use its models in prompts, agents, and evaluations."
---

[Fireworks AI](https://fireworks.ai/): Fireworks AI hosts open models behind an OpenAI-compatible inference API. In GGX, Fireworks AI is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers Fireworks AI as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](../../../register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the key to model code as environment variables, so scoring logic can call Fireworks AI without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Fireworks AI card.
3. Enter your Fireworks AI API key.
4. Save the connection.

GGX provides the key as `FIREWORKS_API_KEY` in model code. The Fireworks AI API is OpenAI-compatible, so scoring logic can use the OpenAI client with the base URL `https://api.fireworks.ai/inference/v1`.

Keys are write-only and stored encrypted.
