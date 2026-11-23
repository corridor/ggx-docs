# Ollama
Source: https://docs.genguardx.ai/integrations/llm-providers/ollama/
Markdown: https://docs.genguardx.ai/integrations/llm-providers/ollama/index.md
Description: Connect Ollama to GGX with a server address and optional API key and use its models in prompts, agents, and evaluations.

[Ollama](https://ollama.com/): Ollama runs open models on a server that you operate and exposes an OpenAI-compatible API. In GGX, Ollama is an LLM provider that you connect once and use for models you register.

## What it does in GGX

- Registers Ollama as an LLM provider in **Org Settings → Integrations**, so its models can be used by [Models](https://docs.genguardx.ai/register-and-refine/inventory-management/model-catalog/) that call it.
- Exposes the server address and key to model code as environment variables, so scoring logic can call Ollama without embedding secrets.
- Registered models take part in GGX simulations, comparisons, approvals, and production monitoring like any other provider.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Providers** group.
2. Click the Ollama card.
3. Enter the base URL of your Ollama server (for example `http://localhost:11434/v1`). The server must be reachable from the GGX API; `localhost` means the machine that runs GGX itself.
4. Enter an API key only if your server requires one; the key is optional.
5. Save the connection.

GGX provides the address as `OLLAMA_BASE_URL` and the key as `OLLAMA_API_KEY` in model code.

Keys are write-only and stored encrypted.
