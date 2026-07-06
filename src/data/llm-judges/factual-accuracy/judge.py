import typing as t

import genguardx as ggx

prompt_template = """\
You are an expert evaluation system specialized in measuring **Factual Accuracy** (also known as faithfulness or groundedness).

Your role is to judge whether the factual claims made in a given RESPONSE are accurate **with respect to the provided CONTEXT**, and to assign a single integer score from 0 to 4.

## What "Factual Accuracy" Means
Factual accuracy measures whether the factual claims in the response are supported by, and consistent with, the information in the CONTEXT. The CONTEXT is the single source of truth. You are checking whether the response is faithful to that source.

This metric is concerned ONLY with factual correctness relative to the context. It is explicitly NOT concerned with:
- **Answer relevancy** — whether the response actually addresses the user's question. A response can be perfectly accurate yet completely off-topic; do NOT lower the factual score for being off-topic, and do NOT raise it for being on-topic.
- Writing style, grammar, tone, fluency, helpfulness, or how completely the question is covered.
- Safety, toxicity, or bias.

## The Context Is the Source of Truth
- Judge claims ONLY against the provided CONTEXT. Do NOT use outside or world knowledge to "correct", "confirm", or override claims, even if you personally believe the context is wrong or outdated.
- A claim is **supported** if the context states it or directly entails it.
- A claim is **contradicted** if the context states something different from or incompatible with the claim.
- A claim is **unsupported / fabricated** if it is absent from the context and cannot be reasonably inferred from it (i.e., a hallucination).

## Judging Principles
- Decompose the response into its individual factual claims and verify each one against the context.
- **Contradicted** claims are the most severe error — they are outright wrong relative to the source.
- **Fabricated / unsupported** claims (hallucinations) also reduce accuracy, even when they sound plausible or are likely true in the real world.
- Subjective statements, opinions, questions, greetings, hedges ("I think", "it may"), and generic filler are NOT factual claims; ignore them when scoring.
- A response that correctly states the context does not contain the requested information makes no false claim and should score high on factual accuracy.
- The USER MESSAGE is provided ONLY to help you interpret what the response is asserting. Do NOT judge how well the response answers it.

## Scoring Scale (0 to 4)
Assign exactly one integer score:

- **0 — Completely inaccurate**: Essentially all factual claims are contradicted by, or fabricated relative to, the context. The response is unfaithful to the source.
  Example — Context: "Q3 revenue was $4.2M." Response: "Q3 revenue was $9M and profit doubled."

- **1 — Mostly inaccurate**: Contains major contradictions or hallucinations; the few supported claims are outweighed by false or unsupported ones.

- **2 — Partially accurate**: A mix of supported and contradicted/unsupported claims. Some key facts are correct, but there are clear factual errors or hallucinations.

- **3 — Mostly accurate**: All core claims are supported by the context, with only minor unsupported details or slight imprecision that does not mislead.

- **4 — Fully accurate**: Every factual claim is fully supported by and consistent with the context. No contradictions and no fabrications.
  Example — Context: "The Eiffel Tower is 330 m tall and located in Paris." Response: "The Eiffel Tower is 330 meters tall and is in Paris."

## Output Format Specification
Return the result as a single **valid JSON object** in plaintext only, with exactly these two keys:

{{
  "score": one integer between 0 and 4,
  "reasoning": "Concise justification (1-2 sentences) explaining the score by referencing which specific claims are supported, contradicted, or unsupported by the context."
}}

Rules:
- "score" MUST be an integer between 0 and 4 (never a float, never below 0, never above 4).
- "reasoning" MUST be a concise string explaining the score.
- Do NOT wrap the JSON in quotes or code fences, and do NOT use escape characters (no '\\n', '\\t').
- Do NOT add any commentary, explanation, or text before or after the JSON object.

## Current task
Evaluate the factual accuracy of the RESPONSE strictly against the CONTEXT.

### CONTEXT (source of truth):
{context}

### USER MESSAGE (for interpretation only):
{user_message}

### RESPONSE:
{response}

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="Factual Accuracy Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def factual_accuracy_prompt(
    user_message: str = None,
    response: str = None,
    context: str = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This prompt creates a factual-accuracy (faithfulness / groundedness) evaluation system that, given a user message, a response, and a context, judges whether the factual claims in the response are supported by the context on a 0-4 scale. It treats the context as the single source of truth and deliberately ignores answer relevancy, style, and safety.

    Required Parameters :
    user_message: The original question or request from the user, used only to interpret what the response is asserting.
    response: The answer/output being evaluated for factual accuracy against the context.
    context: The grounding/source material treated as the source of truth against which the response's claims are checked.

    Output Format :
    Returns a clean JSON object with two keys: an integer "score" (0-4) and a string "reasoning" justifying the score by referencing supported, contradicted, or unsupported claims. The JSON is returned as plaintext without escape characters or surrounding quotes.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab in the lineage view above.
    """
    return prompt.format(user_message=user_message, response=response, context=context)


@ggx.Model.declare(
    name="Factual Accuracy LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def factual_accuracy_llm_as_a_judge(
    user_message: str,
    response: str,
    context: str,
    *,
    cache: dict = {},
) -> t.TypedDict("T", {"score": int, "reasoning": str}, total=False):
    """
    LLM-as-a-Judge that measures factual accuracy (faithfulness / groundedness):
    given a user message, a response, and a context, it scores how well the
    response's factual claims are supported by the context on a 0-4 scale
    (0 = completely inaccurate, 4 = fully accurate) and returns a dict with an
    integer "score" and a string "reasoning".

    The context is treated as the single source of truth. Factual accuracy is
    judged independently of answer relevancy — an on-topic response can still be
    factually inaccurate, and an off-topic response can still be factually
    accurate. Contradictions and fabricated (hallucinated) claims both lower the
    score.
    """
    import time
    import typing as t
    from pydantic import BaseModel, Field

    class FactualAccuracyResult(BaseModel):
        score: int = Field(
            ...,
            ge=0,
            le=4,
            description="Integer 0 (completely inaccurate) to 4 (fully accurate).",
        )
        reasoning: str = Field(
            ...,
            description="Concise 1-2 sentence justification for the score.",
        )

    prompt = factual_accuracy_prompt(
        user_message=user_message, response=response, context=context
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
        response_format=FactualAccuracyResult,
    )

    result: FactualAccuracyResult = completion_response.choices[0].message.parsed
    return result.model_dump()

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(factual_accuracy_llm_as_a_judge)
