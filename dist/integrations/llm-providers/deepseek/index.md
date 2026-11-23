# Deepseek
Source: https://docs.genguardx.ai/integrations/llm-providers/deepseek/
Markdown: https://docs.genguardx.ai/integrations/llm-providers/deepseek/index.md
Description: Connect Deepseek to GGX with an API key and use its models in prompts, agents, and evaluations.

[Deepseek](https://www.deepseek.com/): DeepSeek develops the DeepSeek family of large language models, available through the DeepSeek API. In GGX, Deepseek is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers Deepseek as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](https://docs.genguardx.ai/register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the key to model code as environment variables, so scoring logic can call Deepseek without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Deepseek card.
3. Enter your Deepseek API key.
4. Save the connection.

GGX provides the key as `DEEPSEEK_API_KEY` in model code. The Deepseek API is OpenAI-compatible, so scoring logic can use the OpenAI client with the base URL `https://api.deepseek.com`.

Keys are write-only and stored encrypted.
