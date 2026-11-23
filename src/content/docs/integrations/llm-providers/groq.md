---
title: "Groq"
description: "Connect Groq to GGX with an API key and use its models in prompts, agents, and evaluations."
---

[Groq](https://groq.com/): Groq provides hosted, low-latency inference for open models through an OpenAI-compatible API. In GGX, Groq is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers Groq as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](../../../register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the key to model code as environment variables, so scoring logic can call Groq without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Groq card.
3. Enter your Groq API key.
4. Save the connection.

GGX provides the key as `GROQ_API_KEY` in model code. The Groq API is OpenAI-compatible, so scoring logic can use the OpenAI client with the base URL `https://api.groq.com/openai/v1`.

Keys are write-only and stored encrypted.
