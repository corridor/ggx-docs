---
title: "Meta (Llama)"
description: "Connect Meta's Llama API to GGX with an API key so Llama models can be used as an LLM provider."
---

[Meta](https://llama.developer.meta.com/docs/) offers the Llama family of models through the Llama API. GGX can use it as an LLM provider.

## What it does in GGX

- Registers Meta (Llama) as an LLM provider in **Org Settings → Integrations**.
- Exposes the API key to model code as an environment variable, so models registered in [Models](../../../register-and-refine/inventory-management/model-catalog/) can call Llama without embedding secrets.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Meta card.
3. Enter your Llama API key and save the connection.

GGX provides the key as `LLAMA_API_KEY` in model code. Keys are write-only and stored encrypted.
