# Sending Traces
Source: https://docs.genguardx.ai/agent-observability/sending-traces/
Markdown: https://docs.genguardx.ai/agent-observability/sending-traces/index.md
Description: Send traces to GGX from registered assets, the genguardx Python SDK or any OpenTelemetry exporter. Covers tool spans, custom metadata and tags, and agent framework tracing.

There are four ways to get traces into GGX. They all go through the same intake, so masking, pricing, retention and access rules apply the same way whichever you use.

| Source | How it works |
| --- | --- |
| **Assets registered in GGX** | Agents, Models and other assets registered in GGX produce traces when they run on the platform, as long as your administrator has platform tracing configured. |
| **The GGX Python SDK** | Two lines in your application. Model calls through OpenAI or Anthropic, and agents built with LangChain, LangGraph, LlamaIndex, CrewAI or the OpenAI Agents SDK, are captured automatically. |
| **Any OpenTelemetry exporter** | Point an OTLP/HTTP exporter at `/api/v1/traces/otlp` with your API key. |
| **Langfuse history** | Your administrator can import past traces, sessions and scores from a Langfuse instance. |

## With the Python SDK

Install the extra for the libraries your application uses (see [Frameworks](#frameworks) for the full list), then initialize tracing once at start-up, after any OpenTelemetry setup of your own.

```bash
pip install "genguardx[tracing-openai]"
```

```python
from genguardx import tracing

tracing.init(
    api_key="your-ggx-api-key",        # or the GGX_API_KEY environment variable
    api_url="https://ggx.example.com",  # or GGX_API_URL
    deployment_id=12,                   # or pipeline_version_id=..., or project_id=...
    environment="prod",
    service_name="card-assistant",
)

# Group a conversation into a session and tag who it was for:
with tracing.context(session_id="chat-8841", user_id="cardholder-2207"):
    reply = assistant.respond(message)
```

The scope you name is checked against what your API key may write, so traces can only land in projects you have access to. The SDK never raises into your application: if GGX cannot be reached it logs, backs off when asked to slow down, and carries on.

## Your own tools

Model calls are traced for you, because GGX instruments the model libraries. Your tools are your own functions, so a trace shows the model asking for a tool but not the tool running until you mark it. Mark each tool function with `@tracing.tool`, or wrap the place you call tools with `tracing.trace_tool`.

```python
from genguardx import tracing

@tracing.tool
def lookup_card_status(card_id: str) -> dict:
    return cards.status(card_id)

# Or around one call site that runs many tools:
with tracing.trace_tool(name, args) as call:
    result = registry[name](**args)
    call.record(result)
```

Each call then appears as a tool span with its arguments, its result or error, and its duration, next to the model calls. It counts towards the trace's tool calls, tool time and [agent flags](https://docs.genguardx.ai/agent-observability/agents-and-sessions/#trajectory-flags).

This works the same in agent code running inside GGX and in your own application. Arguments and results are recorded only where content capture is on, and they are [masked](https://docs.genguardx.ai/agent-observability/data-masking/) like every other input and output.

An agent you wrote without a framework is marked the same way, with `@tracing.agent` or `tracing.trace_agent`. See [The agent graph](https://docs.genguardx.ai/agent-observability/agents-and-sessions/#the-agent-graph).

## Custom metadata and tags

A trace can carry your own values next to what GGX captures, such as the customer tier, the application version or an experiment name. There are two places to put them:

| Use | For | How to send it |
| --- | --- | --- |
| **Tags** | Short labels you filter by, such as `beta` or `card-replacement`. | `tags=` on `tracing.init()` or `tracing.context()`, or `tracing.add_tags()`. |
| **Span attributes** | Key and value metadata, such as `customer_tier = "gold"`. | Set an attribute on the current span with the OpenTelemetry API. |

```python
from opentelemetry import trace

from genguardx import tracing

tracing.init(
    api_key="your-ggx-api-key",
    api_url="https://ggx.example.com",
    deployment_id=12,
    tags=["card-replacement"],          # on every span from this process
)

with tracing.context(session_id="chat-8841", tags=["beta"]):
    tracing.add_tags("escalated")       # for the rest of this block

    # Key and value metadata: set it on the span that is running
    span = trace.get_current_span()
    span.set_attribute("customer_tier", "gold")
    span.set_attribute("app.version", "1.2")

    reply = assistant.respond(message)
```

The SDK has no separate metadata argument: metadata is a span attribute, with any key you choose. A value that is the same for the whole process, such as the application version, can be set once as a resource attribute instead, for example through the standard `OTEL_RESOURCE_ATTRIBUTES` environment variable.

The arguments of a tool call need none of this. A function marked with [`@tracing.tool`](#your-own-tools) records its arguments and result on the tool span for you.

Once the trace is in GGX:

- **See it.** Your attributes appear on the span's **Attributes** tab, nested by their dotted names. See [Exploring traces](https://docs.genguardx.ai/agent-observability/exploring-traces/).
- **Search it.** On the Spans tab, query any attribute as `attr.<key>`, for example `attr.app.version = 1.2`.
- **Filter and chart by it.** Promote a key to a [metadata dimension](https://docs.genguardx.ai/agent-observability/search-and-analytics/#metadata-dimensions) and it becomes a sidebar filter, `metadata.<key>` in trace queries and a grouping in Analytics. A project can promote up to 10 keys.

**Caution: Keep personal data out of tags**

Attribute values are [masked](https://docs.genguardx.ai/agent-observability/data-masking/) like inputs and outputs. Tags, user ids and session ids are not, because GGX groups and filters by them. A trace keeps at most 50 tags.

## Frameworks

Agent frameworks are traced one level above the model calls: each chain, graph node, agent, tool and retriever becomes a span, with the model calls it made beneath it.

**Agents running inside GGX** need nothing. Agent code that builds its agent with LangChain or LangGraph is instrumented as soon as it imports LangChain, alongside the OpenAI, Anthropic, Bedrock and Gemini clients, and the run's trace holds every node and tool. A LangGraph graph's nodes appear on the trace's **Graph** view. As with the rest of platform tracing, inputs and outputs are recorded only when your administrator has turned content capture on.

**Your own applications** install the extra for the framework they use. `tracing.init()` defaults to `instrument="auto"`: it turns on every instrumentation that is installed, for every framework and model library that is installed too. `instrument=False` turns none on, if you set instrumentation up yourself.

```bash
pip install "genguardx[tracing-langgraph,tracing-openai]"
```

```python
from genguardx import tracing

tracing.init(api_key="your-ggx-api-key", api_url="https://ggx.example.com", deployment_id=12)
# instrument="auto" is the default: LangGraph and OpenAI are both traced from here on
```

| Framework or library | Extra | Instrumentation it installs |
| --- | --- | --- |
| LangChain | `genguardx[tracing-langchain]` | `openinference-instrumentation-langchain` |
| LangGraph | `genguardx[tracing-langgraph]` | `openinference-instrumentation-langchain` |
| LlamaIndex | `genguardx[tracing-llamaindex]` | `openinference-instrumentation-llama-index` |
| CrewAI | `genguardx[tracing-crewai]` | `openinference-instrumentation-crewai` |
| OpenAI Agents SDK | `genguardx[tracing-openai-agents]` | `openinference-instrumentation-openai-agents` |
| OpenAI | `genguardx[tracing-openai]` | `opentelemetry-instrumentation-openai` |
| Anthropic | `genguardx[tracing-anthropic]` | `opentelemetry-instrumentation-anthropic` |
| All of the above | `genguardx[tracing-all]` | Each of them |

An extra installs the instrumentation only; the framework stays at whatever version you run. You are not limited to this list: any OpenInference or OpenLLMetry instrumentor sends spans GGX reads, as long as it is pointed at the tracer provider `tracing.init()` set up, or at the [OTLP endpoint](#with-any-opentelemetry-exporter) below.

### Each model call is counted once

With a framework and a model library both instrumented, one call is seen twice: LangChain's `ChatOpenAI` step and the OpenAI request inside it. GGX keeps the request from the model library as the model call, because it carries the provider's own token counts, and shows the framework's step as the chain around it. Tokens and cost are counted from the model call alone, in the trace list, analytics and every total. A framework call that no model library recorded is the model call itself.

**Caution: LlamaIndex and CrewAI**

The LlamaIndex and CrewAI instrumentations do not place the model library's request inside their own model-call step, so GGX cannot tell the two apart. If you use `tracing-llamaindex` or `tracing-crewai`, do not also install a model-library extra such as `tracing-openai` (or `tracing-all`), or those calls will be counted twice.

## With any OpenTelemetry exporter

GGX reads the OpenTelemetry GenAI conventions, OpenInference and OpenLLMetry, so spans from most instrumentation libraries arrive with their model, tokens, inputs and errors intact.

| Setting | Value |
| --- | --- |
| Endpoint | `POST https://<your-ggx>/api/v1/traces/otlp` |
| Authentication | `x-api-key: <your GGX API key>` |
| Encoding | OTLP protobuf or JSON, optionally gzip-compressed |
| Scope | Resource attribute `ggx.deployment_id`, `ggx.pipeline_version_id` or `ggx.project_id` |
| Limits | Up to 10,000 spans per request. A busy server answers `429` with `Retry-After`. |

To group a conversation into a [session](https://docs.genguardx.ai/agent-observability/agents-and-sessions/#sessions), send the same `session.id` span attribute on every turn. Custom metadata works the same way as with the SDK: send it as [span attributes](#custom-metadata-and-tags) under your own keys.

## What to read next

- [Data masking](https://docs.genguardx.ai/agent-observability/data-masking/): what GGX hides before a span is stored.
- [Exploring traces](https://docs.genguardx.ai/agent-observability/exploring-traces/): find and read the traces you sent.
- [Scores and feedback](https://docs.genguardx.ai/agent-observability/scores-and-feedback/#relaying-end-user-feedback): score a trace from your application.
