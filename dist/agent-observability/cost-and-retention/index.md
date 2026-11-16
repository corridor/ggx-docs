# Cost and Retention
Source: https://docs.genguardx.ai/agent-observability/cost-and-retention/
Markdown: https://docs.genguardx.ai/agent-observability/cost-and-retention/index.md
Description: How GGX prices LLM calls from your organization's price sheet, flags unpriced models, and handles trace retention, sampling, purge and access.

## Cost

GGX prices every model call from your organization's price sheet, at the rates in force on the day the call ran. Prices are per million tokens and can differ for input, output, cache reads, cache writes and reasoning tokens. Volume tiers can apply higher rates above a prompt size.

- An administrator manages prices under **Org Settings → Cost Configs**.
- A call whose model has no price is marked **unpriced**, never counted as free. A banner on the trace list names the models to add prices for, over the range you are looking at.
- Costs are never added up across currencies; each currency has its own total.
- A model call recorded by both a framework and a model library is priced once, from the model library's record. See [Each model call is counted once](https://docs.genguardx.ai/agent-observability/sending-traces/#each-model-call-is-counted-once).

## Retention and sampling

- **Retention**: spans are kept for 90 days unless your administrator sets a shorter window for a project. A trace's scores and evaluations go with it.
- **Sampling**: a project can keep a share of its new traces rather than all of them. A trace is either kept whole or dropped whole, never partly.
- **Purge**: an organization admin can remove every trace of a project, for example after the project is deleted.

## Access

You see the traces, sessions, scores and evaluations of projects you can read. GGX's own platform traces are visible to organization admins only.

## What to read next

- [Exploring traces](https://docs.genguardx.ai/agent-observability/exploring-traces/#the-trace-list): where cost and unpriced spans show up.
- [Monitors](https://docs.genguardx.ai/agent-observability/monitors/#what-you-can-monitor): alert on cost per currency and token totals.
- [Data masking](https://docs.genguardx.ai/agent-observability/data-masking/): control what content is stored in the first place.
