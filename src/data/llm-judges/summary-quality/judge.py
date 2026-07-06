import typing as t

import genguardx as ggx

prompt_template = """\
# Instruction
You are an expert evaluator of text summaries. You will rate a SUMMARY of a SOURCE TEXT on a single quality aspect: **{aspect}**.

Definition of {aspect}: {aspect_definition}

Rate the summary on {aspect} only, using an integer scale from 1 (very poor) to 5 (excellent). Be generous and not overly strict, and judge this aspect independently of any other quality dimension.

## Scoring Scale
- 1: Very poor on {aspect}.
- 2: Poor — noticeable problems.
- 3: Average — acceptable but with clear gaps.
- 4: Good — minor issues only.
- 5: Excellent — fully satisfies this aspect.

## Input
SOURCE TEXT:
{source_text}

SUMMARY:
{summary}

## Output Format Specification
Return the result as a single **valid JSON object** in plaintext only, with exactly these two keys:

{{
  "score": an integer from 1 to 5,
  "reasoning": "Concise justification for the {aspect} score, citing the specific strengths and weaknesses that drove it."
}}

Rules:
- "score" MUST be an integer between 1 and 5.
- "reasoning" MUST be a concise string.
- Do NOT wrap the JSON in quotes or code fences, and do NOT use escape characters (no '\\n', '\\t').
- Do NOT add any commentary, explanation, or text before or after the JSON object.

## Current task
Evaluate the SUMMARY against the SOURCE TEXT on the {aspect} aspect only.

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="Summary Quality Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def summary_quality_prompt(
    aspect: str = None,
    aspect_definition: str = None,
    source_text: str = None,
    summary: str = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This is a single, aspect-agnostic summary-quality prompt. Given a source text, a summary, and one quality aspect (with its definition), it rates the summary on that one aspect on a 1-5 scale. The judge reuses this same prompt for each aspect — coherence, consistency, fluency, informativeness, and relevance — by filling in the aspect placeholders.

    Required Parameters :
    aspect: The single quality aspect to evaluate (e.g. "coherence", "consistency", "fluency", "informativeness", "relevance").
    aspect_definition: The definition of that aspect, used to anchor the rubric.
    source_text: The original text that was summarized.
    summary: The summary of the source text being evaluated.

    Output Format :
    Returns a clean JSON object with two keys: an integer "score" (1-5) for the given aspect and a string "reasoning". The JSON is returned as plaintext without escape characters or surrounding quotes.

    Reference :
    Li, Li & Tan, "HypoEval: Hypothesis-Guided Evaluation for Natural Language Generation" (2025), arXiv:2504.07174.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab in the lineage view above.
    """
    return prompt.format(
        aspect=aspect,
        aspect_definition=aspect_definition,
        source_text=source_text,
        summary=summary,
    )


@ggx.Model.declare(
    name="Summary Quality LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def summary_quality_llm_as_a_judge(
    source_text: str,
    summary: str,
    *,
    cache: dict = {},
) -> t.TypedDict(
    "T",
    {"score": t.Dict[str, int], "reasoning": t.Dict[str, str]},
    total=False,
):
    """
    LLM-as-a-Judge for summary quality. Given a source text and a summary of it,
    it rates the summary across five independent aspects on a 1-5 scale —
    coherence, consistency, fluency, informativeness, and relevance — with one
    LLM call per aspect using a single, aspect-agnostic prompt.

    Returns a dict with two keys: "score" (a dict mapping each aspect to its 1-5
    integer score) and "reasoning" (a dict mapping each aspect to its
    justification). Each aspect is scored independently; there is no
    overall/aggregate score. Adapted from HypoEval (Li, Li & Tan, 2025,
    arXiv:2504.07174).
    """
    # The five summary-quality aspects and their definitions. Each definition
    # gives the core meaning plus concrete signals for high vs. low scores
    # (distilled from HypoEval's per-aspect rubrics). Each is filled into the
    # single prompt template above, one aspect per LLM call.
    aspect_definitions = {
        "coherence": (
            "Coherence measures the quality of all sentences collectively — how well they "
            "fit together and sound natural as a whole. Score high (4-5) when the summary "
            "uses transitional phrases and cohesive devices to link ideas, is well-organized, "
            "flows smoothly, and is easy to follow. Score low (1-2) when transitions are "
            "abrupt or missing, the narrative is choppy or disjointed, or ideas are poorly "
            "connected. Some transitions but noticeable gaps in cohesion fall in the middle (3)."
        ),
        "consistency": (
            "Consistency measures whether the facts in the summary align with those in the "
            "source, so that all facts are accurately reproduced and no untrue information is "
            "introduced. Score high (4-5) when every claim is faithful to the source, uses "
            "precise terminology consistent with it, and introduces no hallucinations or "
            "invented details. Score low (1-2) for significant factual inaccuracies, "
            "hallucinations, or misleading terminology that misrepresents the source; minor, "
            "non-misleading inaccuracies fall in the middle (3)."
        ),
        "fluency": (
            "Fluency measures the quality of individual sentences — whether they are "
            "well-written, grammatically correct, clear, and readable. Score high (4-5) for "
            "clear, concise, grammatical sentences with varied structure and natural flow. "
            "Score low (1-2) for run-on sentences, overly complex or awkward constructions, "
            "grammatical errors, or vague references that hinder readability. A serviceable mix "
            "with some awkwardness falls in the middle (3)."
        ),
        "informativeness": (
            "Informativeness measures how well the summary captures the key points, main "
            "ideas, and themes of the source, with enough depth and supporting detail. Score "
            "high (4-5) when it comprehensively conveys the main ideas and their significance "
            "with relevant context, synthesizing rather than merely restating. Score low (1-2) "
            "when it omits the main ideas or mentions them only vaguely. Identifying the main "
            "ideas but without depth or supporting detail falls in the middle (3)."
        ),
        "relevance": (
            "Relevance measures how well the summary captures the key points of the source, "
            "considering whether all and only the important aspects are included. Score high "
            "(4-5) when it captures all the main topics concisely and comprehensively, without "
            "unnecessary elaboration, irrelevant information, or redundancy. Score low (1-2) "
            "when it is off-topic, misses key points, or is overly verbose with irrelevant "
            "content. Mostly on-point but with some omissions or redundancy falls in the middle (3)."
        ),
    }

    import time
    import typing as t
    from pydantic import BaseModel, Field

    class AspectResult(BaseModel):
        score: int = Field(
            ...,
            ge=1,
            le=5,
            description="Integer 1 (very poor) to 5 (excellent) for this aspect.",
        )
        reasoning: str = Field(
            ...,
            description="Concise justification for this aspect's score.",
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

    # One call per aspect, reusing the single aspect-agnostic prompt. Both the
    # scores and the reasonings are collected per aspect into a single dict each.
    score: dict = {}
    reasoning: dict = {}
    for aspect, definition in aspect_definitions.items():
        prompt = summary_quality_prompt(
            aspect=aspect,
            aspect_definition=definition,
            source_text=source_text,
            summary=summary,
        )
        completion_response = llm_client.completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format=AspectResult,
        )
        result: AspectResult = completion_response.choices[0].message.parsed
        score[aspect] = result.score
        reasoning[aspect] = result.reasoning

    return {"score": score, "reasoning": reasoning}

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(summary_quality_llm_as_a_judge)
