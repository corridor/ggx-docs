# Vertex AI Agent Playbooks
Source: https://docs.genguardx.ai/integrations/agent-studios/vertex-ai-agent-playbooks/
Markdown: https://docs.genguardx.ai/integrations/agent-studios/vertex-ai-agent-playbooks/index.md
Description: Connect Google Cloud Vertex AI Agent Playbooks to GGX to register playbook-based conversational agents for testing and governance.

[Vertex AI Agent Playbooks](https://cloud.google.com/vertex-ai) is Google Cloud's framework for building conversational AI agents. GGX uses it to register playbook agents for testing and governance.

## What it does in GGX

- Register an agent built on Vertex AI Agent Playbooks in GGX, so it can be tested, evaluated, and governed like any other agent.
- GGX provides starter run logic for Vertex AI Agent Playbooks that sends a user message to the agent and returns its reply, which you adapt to your agent.
- Once registered, the agent can be used in simulations, judges, and reviews alongside your other agents.

## How to connect

1. In GGX, open **Org Settings → Integrations → Agent studios** and select **Vertex AI Agent Playbooks**.
2. Provide the API key and endpoint of your Vertex AI project.
3. Save. Authorized users can then create an agent that uses Vertex AI Agent Playbooks.

## GenGuardX on Google Cloud

GenGuardX is listed on [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/corridorgenguardx-public/corridorggx).
