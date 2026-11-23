---
title: "TypeSafe AI"
description: "Connect TypeSafe AI to GGX with an API key so it can be used as an LLM provider."
---

[TypeSafe AI](https://developer.konghq.com/ai-gateway/ai-providers/typesafe/) is an AI provider that can be used as an LLM provider in GGX.

## What it does in GGX

- Registers TypeSafe AI as an LLM provider in **Org Settings → Integrations**.
- Exposes the API key to model code as an environment variable, so models registered in [Models](../../../register-and-refine/inventory-management/model-catalog/) can call it without embedding secrets.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the TypeSafe AI card.
3. Enter your TypeSafe AI API key and save the connection.

GGX provides the key as `TYPESAFE_API_KEY` in model code. Keys are write-only and stored encrypted.
