# NVIDIA NIM
Source: https://docs.genguardx.ai/integrations/llm-gateways/nvidia-nim/
Markdown: https://docs.genguardx.ai/integrations/llm-gateways/nvidia-nim/index.md
Description: Connect NVIDIA NIM to GGX with an API key and route model calls through it.

[NVIDIA NIM](https://build.nvidia.com/): NVIDIA NIM provides inference microservices and hosted endpoints for models in the NVIDIA catalog. In GGX, it is an LLM gateway: models registered in GGX can call it, and it routes to the models it has access to. See [LLM Gateways](https://docs.genguardx.ai/integrations/llm-gateways/) for the general pattern.

## What it does in GGX

- Registers NVIDIA NIM under **LLM Gateways** in **Org Settings → Integrations**.
- Exposes the credentials to model code as environment variables, so models registered in [Models](https://docs.genguardx.ai/register-and-refine/inventory-management/model-catalog/) can call the gateway without embedding secrets.
- Models served through the gateway take part in GGX simulations, comparisons, approvals, and monitoring.

## How to connect

1. Open **Org Settings → Integrations** from the profile menu and find the **LLM Gateways** group.
2. Click the NVIDIA NIM card.
3. Enter your NVIDIA API key and the endpoint of the model, taken from the model endpoint you copy from the NVIDIA catalog or your own NIM deployment.
4. Save the connection.

GGX provides `NVIDIA_API_KEY` and `NVIDIA_NIM_ENDPOINT` in model code. Secrets are write-only and stored encrypted.

## Notes

A gateway can serve a different model than the one you ask for (fallbacks, aliases, routing). Record what sits behind the gateway in the model description and risk assessment.
