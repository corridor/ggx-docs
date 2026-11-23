# LM Studio
Source: https://docs.genguardx.ai/integrations/llm-providers/lm-studio/
Markdown: https://docs.genguardx.ai/integrations/llm-providers/lm-studio/index.md
Description: Connect LM Studio to GGX with a server address and optional API key and use its models in prompts, agents, and evaluations.

[LM Studio](https://lmstudio.ai/): LM Studio runs models locally and can serve them through an OpenAI-compatible local server. In GGX, LM Studio is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers LM Studio as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](https://docs.genguardx.ai/register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the server address and key to model code as environment variables, so scoring logic can call LM Studio without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the LM Studio card.
3. Enter the base URL of your LM Studio server (for example `http://localhost:1234/v1`). The server must be reachable from the GGX API; `localhost` means the machine that runs GGX itself.
4. Enter an API key only if your server requires one; the key is optional.
5. Save the connection.

GGX provides the address as `LMSTUDIO_BASE_URL` and the key as `LM_API_TOKEN` in model code.

Keys are write-only and stored encrypted.
