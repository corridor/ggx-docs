import typing as t

import genguardx as ggx

prompt_template = """\
You are an expert evaluation system specialized in judging **Tool Call Accuracy** for an LLM agent.

Your role is to decide whether the tool calls produced by the agent for the given USER QUERY are correct given the available TOOL DEFINITIONS and the INTENDED PIPELINE USE. You will return a binary accuracy verdict (1 = fully correct, 0 = not fully correct), a short reasoning, and — when the verdict is 0 — a single failure category from the allowed list.

## What "Tool Call Accuracy" Means
A set of tool calls is **accurate (1)** only if ALL of the following hold:
- Every tool that should have been called (per the intended pipeline use and the query) was called.
- No tool was called that shouldn't have been (no spurious / extra calls).
- Each call selects the right tool for its sub-task.
- The arguments to each tool match the user's intent AND conform to the tool's definition (correct keys, correct value types, semantically correct values pulled from the query / pipeline context).
- The order of calls respects any sequential dependencies described in the intended pipeline use. When the pipeline explicitly allows parallel / order-independent calls, order does not matter.
- Every tool name used actually exists in the TOOL DEFINITIONS. A tool name that is not defined is a hallucinated tool.

If ANY of the above is violated, the verdict is **0**.

A correct edge case: if the query does NOT require any tool calls and the agent made none, that is **accurate (1)**. If the query DID require tool calls and the agent made none, that is **0** with category "No Tool Calls Made".

## Judging Principles
- Judge ONLY against the provided TOOL DEFINITIONS and INTENDED PIPELINE USE. Do not invent tools, arguments, or workflow steps that are not described.
- Do NOT penalize stylistic differences (e.g. equivalent phrasings of the same argument value) as long as the semantic intent matches.
- Be strict about argument correctness: a wrong city, wrong date, wrong filter value, or a missing required argument all count as "Wrong Arguments".
- If multiple things are wrong, pick the SINGLE category that best characterizes the most impactful failure. Prefer categories higher in the list when in doubt.

## Allowed Failure Categories
You MUST pick exactly one of the following when the verdict is 0. Use the strings EXACTLY as written:
{failure_categories_block}

When the verdict is 1 (fully correct), set "failure_category" to null.

## Output Format Specification
Return the result as a single **valid JSON object** in plaintext only, with exactly these three keys:

{{
  "accuracy": 0 or 1,
  "reasoning": "Concise 1-3 sentence justification referencing the specific tool call(s) and argument(s) that drove the verdict.",
  "failure_category": one of the allowed categories above, or null when accuracy is 1
}}

Rules:
- "accuracy" MUST be the integer 0 or the integer 1 (never a float, never a string).
- "reasoning" MUST be a concise string.
- "failure_category" MUST be either null (when accuracy is 1) or one of the exact category strings listed above (when accuracy is 0).
- Do NOT wrap the JSON in code fences and do NOT add commentary before or after the JSON object.

## Current task

### USER QUERY:
{query}

### TOOL DEFINITIONS (the tools the agent has available, with their argument schemas):
{tool_definitions}

### INTENDED PIPELINE USE (how the tools are expected to be used to satisfy the query):
{intended_pipeline_use}

### ACTUAL TOOL CALLS MADE BY THE AGENT:
{actual_tool_calls}

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="Tool Call Accuracy Judge Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def tool_call_accuracy_judge_prompt(
    query: str = None,
    actual_tool_calls: str = None,
    tool_definitions: str = None,
    intended_pipeline_use: str = None,
    failure_categories: t.Optional[t.List[str]] = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    Builds the LLM-as-a-Judge prompt for evaluating whether an agent's tool calls
    correctly satisfy a user query, given the available tool definitions and the
    intended pipeline use. The judge returns a binary accuracy verdict (0/1), a
    reasoning string, and — for failures — a single category from the configured
    failure category list.

    Required Parameters :
    query: The original user query the agent was responding to.
    actual_tool_calls: The list of tool calls made by the agent (each typically
        a dict with "name" and "arguments"). Strings are passed through as-is;
        other types are JSON-serialized for the prompt.
    tool_definitions: The catalog of available tools and their argument schemas.
        Strings are passed through as-is; structured values are JSON-serialized.
    intended_pipeline_use: Natural-language description of how the tools are
        expected to be orchestrated to satisfy the query (including any ordering
        constraints).
    failure_categories: Optional list of allowed failure category labels. When
        omitted, DEFAULT_FAILURE_CATEGORIES is used.

    Output Format :
    Returns a clean JSON object with three keys: integer "accuracy" (0 or 1),
    string "reasoning", and "failure_category" (one of the allowed labels, or
    null when accuracy is 1). Returned as plaintext without code fences.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents"
    tab in the lineage view above.
    """

    import json

    def _format_failure_categories(categories):
        return "\n".join(f"- {c}" for c in categories)

    def _stringify(value):
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value, indent=2, default=str, sort_keys=False)
        except TypeError:
            return repr(value)

    DEFAULT_FAILURE_CATEGORIES = [
        "No Tool Calls Made",
        "Extra Tool Calls Made",
        "Missing Required Tool Calls",
        "Wrong Tool Selected",
        "Wrong Arguments",
        "Wrong Tool Call Order",
        "Hallucinated Tool",
    ]
    categories = failure_categories or DEFAULT_FAILURE_CATEGORIES
    return prompt.format(
        query=query,
        tool_definitions=_stringify(tool_definitions),
        intended_pipeline_use=intended_pipeline_use,
        actual_tool_calls=_stringify(actual_tool_calls),
        failure_categories_block=_format_failure_categories(categories),
    )


@ggx.Model.declare(
    name="Tool Call Accuracy LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def tool_call_accuracy_llm_as_a_judge(
    query: str,
    actual_tool_calls: str,
    intended_pipeline_use: str,
    tool_definitions: str = None,
    failure_categories: t.Optional[t.List[str]] = None,
    *,
    cache: dict = {},
) -> t.TypedDict(
    "T",
    {"accuracy": int, "reasoning": str, "failure_category": str},
    total=False,
):
    """
    LLM-as-a-Judge for tool call accuracy. There is no reference set of tool
    calls — the judge decides correctness purely from the user query, the
    available tool definitions, and a description of the intended pipeline use.

    Inputs:
    - query: the original user query.
    - actual_tool_calls: the tool calls the agent actually made.
    - tool_definitions: catalog of available tools with their argument schemas.
    - intended_pipeline_use: description of how the tools should be orchestrated
      (including any ordering constraints).
    - failure_categories: optional override for the list of failure labels the
      judge may return. Defaults to DEFAULT_FAILURE_CATEGORIES (No Tool Calls
      Made, Extra Tool Calls Made, Missing Required Tool Calls, Wrong Tool
      Selected, Wrong Arguments, Wrong Tool Call Order, Hallucinated Tool).

    Returns a dict with:
    - "accuracy": 1 if fully correct, 0 otherwise.
    - "reasoning": short justification grounded in specific calls / arguments.
    - "failure_category": one of the configured labels when accuracy is 0;
      null when accuracy is 1.
    """
    import time
    import typing as t
    from pydantic import BaseModel, Field

    class ToolCallAccuracyResult(BaseModel):
        accuracy: int = Field(
            ...,
            ge=0,
            le=1,
            description="1 if the tool calls are fully correct, 0 otherwise.",
        )
        reasoning: str = Field(
            ...,
            description="Concise 1-3 sentence justification for the verdict.",
        )
        failure_category: t.Optional[str] = Field(
            None,
            description="One of the allowed failure labels when accuracy is 0; null when accuracy is 1.",
        )

    prompt = tool_call_accuracy_judge_prompt(
        query=query,
        actual_tool_calls=actual_tool_calls,
        tool_definitions=tool_definitions,
        intended_pipeline_use=intended_pipeline_use,
        failure_categories=failure_categories,
    )

    # ---------------------------------------------------------
    # 1. Model & Provider Configuration
    # To change the provider, update the `provider_name` and `model_name`.
    # For example, to switch to AWS Bedrock:
    # provider_name = "bedrock"
    # model_name = "anthropic.claude-4-5-sonnet-20250219-v1:0"
    # ---------------------------------------------------------
    provider_name = "gemini"
    model_name = "gemini-3.5-flash"
    cache_key = f"llm_client_{provider_name}"

    # ---------------------------------------------------------
    # 2. Client Caching & Time-Based Refresh Mechanism
    # ---------------------------------------------------------
    # This block checks if the client exists in the dictionary.
    # If implementing a time-based refresh (TTL), you would store a tuple
    # or dict with the instantiation time, e.g.:
    #
    # ttl_seconds = 3600 # 1 hour
    # current_time = time.time()
    # if cache_key in cache:
    #     client, created_at = cache[cache_key]
    #     if current_time - created_at > ttl_seconds:
    #         del cache[cache_key] # Expire the cache
    #
    # if cache_key not in cache:
    #     cache[cache_key] = (AnyLLM.create(provider=provider_name), current_time)
    #
    # llm_client = cache[cache_key][0]
    # ---------------------------------------------------------

    # Standard caching (without TTL implementation)
    if cache_key not in cache:
        cache[cache_key] = AnyLLM.create(provider=provider_name)

    llm_client = cache[cache_key]

    completion_response = llm_client.completion(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format=ToolCallAccuracyResult,
    )

    result: ToolCallAccuracyResult = completion_response.choices[0].message.parsed
    return result.model_dump()

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(tool_call_accuracy_llm_as_a_judge)
