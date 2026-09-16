# GGX Integrations
Source: https://docs.genguardx.ai/integrations/
Markdown: https://docs.genguardx.ai/integrations/index.md
Description: Connect GGX with LLM providers, LLM gateways, observability tools, agent frameworks, report providers, voice providers, and SSO systems across the AI lifecycle.
GGX is built with extensibility in mind and supports a wide range of integrations that allow you to seamlessly plug into existing workflows and tools.

These integrations are organized into the following categories:

1. **LLM Providers:**  
   Connect to popular foundational models from leading providers to power your generative experiences.  
   Examples: [OpenAI](https://openai.com/), [Google Vertex AI](https://cloud.google.com/vertex-ai),[Azure AI](https://azure.microsoft.com/),[Amazon Bedrock](https://aws.amazon.com/bedrock/), [DeepSeek](https://www.deepseek.com/), [Anthropic](https://www.anthropic.com/), [HuggingFace](https://huggingface.co/), [Nvidia NIM](https://www.nvidia.com/en-us/ai/), [GitHub Models](https://github.com/marketplace/models)

2. **LLM Gateways:**  
   Register an LLM gateway in the GGX Model Registry, then route GGX prompts, RAGs, pipelines, simulations, and monitoring jobs to any LLM the gateway has access to.  
   Examples: [LiteLLM](llm-gateways/litellm/), [Portkey](llm-gateways/portkey/), [OpenRouter](llm-gateways/openrouter/), [Cloudflare AI Gateway](llm-gateways/cloudflare-ai-gateway/), [Databricks AI Gateway](llm-gateways/databricks-ai-gateway/)

3. **Observability:**  
   Connect AI traces, logs, scores, alerts, and review signals to GGX so monitoring feeds judges, human review, ground truth, bug categorization, and lifecycle governance.  
   Examples: [LangSmith](observability/langsmith/), [Arize Phoenix](observability/arize-phoenix/), [Langfuse](observability/langfuse/), [Humanloop](observability/humanloop/), [Datadog](observability/datadog/)

4. **Agent Providers & Frameworks:**  
   Leverage pre-built agent providers or bring your own orchestration frameworks to create and manage intelligent, multi-step agent workflows with minimal setup.  
   Examples: [Vertex AI Agent Playbooks](https://cloud.google.com/dialogflow/cx/docs/concept/playbook), [AgentForce (Salesforce)](https://www.salesforce.com/in/agentforce/), [Microsoft Copilot Studio](https://www.microsoft.com/en-us/microsoft-365-copilot/microsoft-copilot-studio), [Vapi AI](https://vapi.ai/),[GitHub Copilot](https://github.com/features/copilot), [Amazon Lex](https://aws.amazon.com/lex/), [CustomGPT](https://customgpt.ai/)

5. **Report Providers:**  
   Plug in evaluation tools to assess your data, RAGs, pipelines, agents, etc. effectively.  
   Examples: [CleanLabs](https://cleanlabs.ai/), [Perspective API](https://perspectiveapi.com/)

6. **Voice Providers:**
   Setup integrations to services that provide speech-to-text, text-to-speech, Voice Agents
   Examples: [Deepgram](https://deepgram.com/)

7. **Single Sign-On (SSO) Integrations:**
   Setup integrations to services for seamless Authentication and Authorization
   Examples: [Google Workspace](https://workspace.google.com/), [Auth0 (by Okta)](https://auth0.com/), [WorkOS](https://workos.com/), [OneLogin](https://www.onelogin.com/)

## Observability and closed-loop monitoring

AI observability platforms are valuable because they collect production traces, scores, feedback, and alerts. GGX makes those signals operational across the AI lifecycle.

Traces from tools such as LangSmith, Arize Phoenix, Langfuse, Humanloop, and Datadog can be connected to GGX. Once connected, GGX can run automated judges and route selected interactions to human review. Positive reviews can be promoted into ground truth. Negative reviews can become bugs or findings. Repeated issues can be grouped into common failure categories.

This reduces the review funnel and makes monitoring useful beyond dashboards. Monitoring evidence starts to power better datasets, better judges, clearer approval evidence, and more targeted fixes before the next deployment.