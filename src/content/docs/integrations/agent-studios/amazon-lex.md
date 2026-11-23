---
title: "Amazon Lex"
description: "Connect Amazon Lex bots to GGX to register conversational agents and test them with GGX simulations, judges, and reviews."
---

[Amazon Lex](https://aws.amazon.com/lex/) is an AWS service for building conversational interfaces. GGX uses it to register Lex V2 bots for testing and governance.

## What it does in GGX

- Register an agent built on Amazon Lex in GGX, so it can be tested, evaluated, and governed like any other agent.
- GGX provides starter run logic for Amazon Lex that sends a user message to the agent and returns its reply, which you adapt to your agent.
- Once registered, the agent can be used in simulations, judges, and reviews alongside your other agents.

## How to connect

1. In GGX, open **Org Settings → Integrations → Agent studios** and select **Amazon Lex**.
2. Provide your AWS connection details. Set the bot ID and bot alias ID in the agent's run logic.
3. Save. Authorized users can then create an agent that uses Amazon Lex.

## GenGuardX on AWS

GenGuardX is listed on [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-wp7rj5r7vf33u).

