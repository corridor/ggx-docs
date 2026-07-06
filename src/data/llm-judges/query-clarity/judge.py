import typing as t

import genguardx as ggx

prompt_template = """\
# Instruction
You are an expert evaluator. Rate the quality of the user QUERY based on its clarity, specificity, and coherence.

Use the following 5-point rating scale:

- very poor (score 1): The QUERY is unclear, vague, or incoherent. It lacks essential information and context.
- poor (score 2): The QUERY is somewhat unclear or lacks important details. It requires significant clarification.
- average (score 3): The QUERY is moderately clear and specific. It may require some additional information for a complete understanding.
- good (score 4): The QUERY is clear, specific, and mostly well-formed. It provides sufficient context for understanding the user's intent.
- excellent (score 5): The QUERY is very clear, specific, and well-articulated. It contains all the necessary information and context for providing a comprehensive response.

## Input
QUERY: {query}

## Output Format Specification
First assess the QUERY, highlighting its strengths and/or weaknesses. Then assign a rating from the scale above.

Return the result as a single **valid JSON object** in plaintext only, with exactly these three keys:

{{
  "score": an integer from 1 to 5,
  "rating": one of "very poor", "poor", "average", "good", "excellent",
  "reasoning": "Concise assessment highlighting the strengths and/or weaknesses of the QUERY that justify the rating."
}}

Rules:
- "score" MUST be an integer between 1 and 5, and MUST correspond to "rating" (very poor = 1, poor = 2, average = 3, good = 4, excellent = 5).
- "rating" MUST be exactly one of the five labels above.
- "reasoning" MUST be a concise string.
- Do NOT wrap the JSON in quotes or code fences, and do NOT use escape characters (no '\\n', '\\t').
- Do NOT add any commentary, explanation, or text before or after the JSON object.

## Current task
Evaluate the clarity, specificity, and coherence of the QUERY above.

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="Query Clarity Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def query_clarity_prompt(
    query: str = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This prompt creates a query-quality evaluation system that rates a user QUERY on its clarity, specificity, and coherence using a 5-point Likert scale (very poor to excellent). It is adapted from the Magpie query-quality judge.

    Required Parameters :
    query: The user query / prompt whose clarity and specificity are being evaluated.

    Output Format :
    Returns a clean JSON object with three keys: an integer "score" (1-5), a "rating" label (one of very poor, poor, average, good, excellent), and a string "reasoning" assessing the query's strengths and weaknesses. The JSON is returned as plaintext without escape characters or surrounding quotes.

    Reference :
    Xu et al., "Magpie: Alignment Data Synthesis from Scratch by Prompting Aligned LLMs with Nothing" (2024), arXiv:2406.08464.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab in the lineage view above.
    """
    return prompt.format(query=query)


@ggx.Model.declare(
    name="Query Clarity LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def query_clarity_llm_as_a_judge(
    query: str,
    *,
    cache: dict = {},
) -> t.TypedDict("T", {"score": int, "rating": str, "reasoning": str}, total=False):
    """
    LLM-as-a-Judge that rates the quality of a user query on its clarity,
    specificity, and coherence using a 5-point Likert scale. It returns a dict
    with an integer "score" (1 = very poor, 5 = excellent), a "rating" label
    (very poor, poor, average, good, excellent), and a short "reasoning"
    assessing the query's strengths and weaknesses.

    Adapted from the Magpie query-quality judge (Xu et al., 2024,
    arXiv:2406.08464).
    """
    import time
    import typing as t
    from pydantic import BaseModel, Field

    class QueryClarityResult(BaseModel):
        score: int = Field(
            ...,
            ge=1,
            le=5,
            description="Integer 1 (very poor) to 5 (excellent).",
        )
        rating: t.Literal[
            "very poor", "poor", "average", "good", "excellent"
        ] = Field(
            ...,
            description="Likert label matching the score.",
        )
        reasoning: str = Field(
            ...,
            description="Concise assessment of the query's strengths and weaknesses.",
        )

    prompt = query_clarity_prompt(query=query)

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
        response_format=QueryClarityResult,
    )

    result: QueryClarityResult = completion_response.choices[0].message.parsed
    return result.model_dump()

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(query_clarity_llm_as_a_judge)
