# Vapi AI
Source: https://docs.genguardx.ai/integrations/agent-studios/vapi-ai/
Markdown: https://docs.genguardx.ai/integrations/agent-studios/vapi-ai/index.md
Description: Connect Vapi to GGX to register Vapi assistants as chat agents and test them with GGX simulations, judges, and reviews.

[Vapi](https://vapi.ai/) is a platform for building AI assistants. GGX uses it to register Vapi assistants for testing and governance, sending messages to the assistant in a chat session.

## What it does in GGX

- Register an agent built on Vapi AI in GGX, so it can be tested, evaluated, and governed like any other agent.
- GGX provides starter run logic for Vapi AI that sends a user message to the agent and returns its reply, which you adapt to your agent.
- Once registered, the agent can be used in simulations, judges, and reviews alongside your other agents.

## How to connect

1. In GGX, open **Org Settings → Integrations → Agent studios** and select **Vapi AI**.
2. Provide your Vapi API key and, if needed, the endpoint. Set the assistant ID in the agent's run logic.
3. Save. Authorized users can then create an agent that uses Vapi AI.
