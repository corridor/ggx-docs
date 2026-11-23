# CustomGPT
Source: https://docs.genguardx.ai/integrations/agent-studios/customgpt/
Markdown: https://docs.genguardx.ai/integrations/agent-studios/customgpt/index.md
Description: Connect CustomGPT to GGX to register CustomGPT agents and test them with GGX simulations, judges, and reviews.

[CustomGPT](https://customgpt.ai/) is a platform for building AI agents from your own content. GGX uses it to register CustomGPT agents for testing and governance.

## What it does in GGX

- Register an agent built on CustomGPT in GGX, so it can be tested, evaluated, and governed like any other agent.
- GGX provides starter run logic for CustomGPT that sends a user message to the agent and returns its reply, which you adapt to your agent.
- Once registered, the agent can be used in simulations, judges, and reviews alongside your other agents.

## How to connect

1. In GGX, open **Org Settings → Integrations → Agent studios** and select **CustomGPT**.
2. Provide your CustomGPT API key. Set the project ID in the agent's run logic.
3. Save. Authorized users can then create an agent that uses CustomGPT.
