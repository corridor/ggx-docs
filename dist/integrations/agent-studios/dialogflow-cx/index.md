# Dialogflow CX
Source: https://docs.genguardx.ai/integrations/agent-studios/dialogflow-cx/
Markdown: https://docs.genguardx.ai/integrations/agent-studios/dialogflow-cx/index.md
Description: Connect Google Cloud Dialogflow CX to GGX to register conversational agents and test them with GGX simulations, judges, and reviews.

[Dialogflow CX](https://cloud.google.com/dialogflow/cx/docs) is Google Cloud's service for building conversational AI agents. GGX uses it to register Dialogflow CX agents for testing and governance.

## What it does in GGX

- Register an agent built on Dialogflow CX in GGX, so it can be tested, evaluated, and governed like any other agent.
- GGX provides starter run logic for Dialogflow CX that sends a user message to the agent and returns its reply, which you adapt to your agent.
- Once registered, the agent can be used in simulations, judges, and reviews alongside your other agents.

## How to connect

1. In GGX, open **Org Settings → Integrations → Agent studios** and select **Dialogflow CX**.
2. Paste the content of your Google Cloud credentials JSON file. Set the agent details in the agent's run logic.
3. Save. Authorized users can then create an agent that uses Dialogflow CX.

## GenGuardX on Google Cloud

GenGuardX is listed on [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/corridorgenguardx-public/corridorggx).
