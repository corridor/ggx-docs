---
title: "MedBAR"
description: "Connect MedBAR to GGX with an API key to use its question plans and medical evaluations as external evaluation signals."
---

[MedBAR](https://www.medbar.ai/) provides question plans and medical evaluations. GGX uses it as an evaluation provider for healthcare AI.

## What it does in GGX

- Use MedBAR's question plans and medical evaluations as an external evaluation provider (listed under **Judges** in Org Settings).

## How to connect

1. In GGX, open **Org Settings → Integrations → Judges** and select **MedBAR**.
2. Enter your MedBAR API key (it starts with `mk_`) and the endpoint, then save.

## Notes

- A project can use its own credentials instead of the organization's.
