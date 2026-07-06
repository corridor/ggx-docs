import typing as t

import genguardx as ggx

prompt_template = """\
You are an advanced PII (Personally Identifiable Information) detection system.
Your job is to scan a single block of text and identify every span that
corresponds to one of the requested PII categories, mirroring the behaviour of
Microsoft Presidio.

## PII categories to detect
Detect ONLY spans that belong to one of the following entity types. Use the
exact type name shown in UPPER_SNAKE_CASE in your output:

{entity_types}

If a category like "address" or "license number" is requested, treat it as the
UPPER_SNAKE_CASE form (e.g. ADDRESS, LICENSE_NUMBER) and tag matches with that
type.

## Rules
- Only flag substrings that literally appear in the input text. The "value" you
  return MUST be an exact, character-for-character substring of the input.
- Do not invent, normalise, or reformat the matched value.
- Assign a "score" between 0.0 and 1.0 reflecting your confidence that the span
  is genuinely PII of that type.
- A single span maps to exactly one entity type. If unsure between two types,
  pick the most specific one.
- Do not flag spans whose type is not in the requested list above.

## Output Format Specification
Return the result as a single valid JSON object in plaintext only, with exactly
these keys:

{{
  "entities": [
    {{"type": "EMAIL_ADDRESS", "score": 0.95, "value": "jane@acme.com"}}
  ],
  "has_pii": true,
  "num_pii_entities": 1,
  "pii_types": ["EMAIL_ADDRESS"]
}}

Where:
- "entities" is a list with one object per detected span: {{"type", "score", "value"}}.
- "has_pii" is true when at least one entity was detected, otherwise false.
- "num_pii_entities" is the integer count of detected entities.
- "pii_types" is the sorted list of unique entity types detected.

Rules for the JSON:
- Use the exact key names shown above.
- "score" must be a float between 0.0 and 1.0.
- If no PII is found, return {{"entities": [], "has_pii": false,
  "num_pii_entities": 0, "pii_types": []}}.
- Do NOT wrap the JSON in quotes or code fences, and do NOT add any commentary,
  explanation, or text before or after the JSON.

## Current task
Scan the following text for the requested PII categories:

{text}

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="PII Detection Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def pii_detection_prompt(
    text: str = None,
    entity_types: t.Optional[t.List[str]] = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This prompt drives an LLM-as-a-Judge that detects Personally Identifiable
    Information (PII) in free-form text and returns findings in the same
    structured shape that Microsoft Presidio produces (entities, has_pii,
    num_pii_entities, pii_types).

    Required Parameters :
    text: The free-form text to scan for PII.

    Optional Parameters :
    entity_types: List of PII categories to detect. When omitted it defaults to
      EMAIL_ADDRESS, PHONE_NUMBER, ADDRESS and LICENSE_NUMBER.

    Output Format :
    Returns a clean JSON object (as plaintext) with the keys entities, has_pii,
    num_pii_entities and pii_types.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab
    in the lineage view above.
    """
    # Default set of PII categories to look for when the caller does not provide
    # their own list.
    DEFAULT_ENTITY_TYPES = [
        "EMAIL_ADDRESS",
        "PHONE_NUMBER",
        "ADDRESS",
        "LICENSE_NUMBER",
    ]
    entities_to_use = entity_types if entity_types else DEFAULT_ENTITY_TYPES
    formatted_entity_types = "\n".join(f"- {et}" for et in entities_to_use)
    return prompt.format(
        text=text,
        entity_types=formatted_entity_types,
    )


@ggx.Model.declare(
    name="PII Detection LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def pii_detection_llm_as_a_judge(
    text: str,
    entity_types: t.Optional[t.List[str]] = None,
    *,
    cache: dict = {},
) -> t.TypedDict(
    "T",
    {
        "entities": t.List[dict],
        "has_pii": bool,
        "num_pii_entities": int,
        "pii_types": t.List[str],
    },
    total=False,
):
    """
    LLM-as-a-Judge that detects PII (Personally Identifiable Information) in a
    block of text and returns findings in the same shape as Microsoft Presidio,
    so the two are interchangeable downstream.

    For each detected span it returns the entity type (UPPER_SNAKE_CASE), a
    confidence "score" (0.0-1.0) and the exact matched "value" substring, along
    with the summary fields "has_pii", "num_pii_entities" and "pii_types". The
    set of categories to look for is configurable via ``entity_types`` and
    defaults to EMAIL_ADDRESS, PHONE_NUMBER, ADDRESS and LICENSE_NUMBER.
    Empty / None text returns an empty result.
    """
    import time
    import typing as t
    from pydantic import BaseModel, Field

    class PIIEntity(BaseModel):
        type: str = Field(
            ...,
            description="Detected PII entity type in UPPER_SNAKE_CASE (e.g. EMAIL_ADDRESS).",
        )
        score: float = Field(
            ...,
            ge=0.0,
            le=1.0,
            description="Confidence (0.0-1.0) that the span is PII of this type.",
        )
        value: str = Field(
            ...,
            description="Exact, verbatim substring from the input that was flagged.",
        )

    class PIIDetectionResult(BaseModel):
        entities: t.List[PIIEntity] = Field(
            default_factory=list,
            description="One entry per detected PII span.",
        )
        has_pii: bool = Field(
            ...,
            description="True when at least one PII entity was detected.",
        )
        num_pii_entities: int = Field(
            ...,
            ge=0,
            description="Count of detected PII entities.",
        )
        pii_types: t.List[str] = Field(
            default_factory=list,
            description="Sorted, unique list of detected entity types.",
        )

    empty_result = {
        "entities": [],
        "has_pii": False,
        "num_pii_entities": 0,
        "pii_types": [],
    }

    if not text:
        return empty_result

    prompt = pii_detection_prompt(text=text, entity_types=entity_types)

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
        response_format=PIIDetectionResult,
    )

    result: PIIDetectionResult = completion_response.choices[0].message.parsed

    # Derive the summary fields from the detected spans so the counts and types
    # always stay consistent with the returned entities (Presidio-compatible).
    entities = [e.model_dump() for e in result.entities]
    pii_types = sorted({e["type"] for e in entities if e.get("type")})
    return {
        "entities": entities,
        "has_pii": len(entities) > 0,
        "num_pii_entities": len(entities),
        "pii_types": pii_types,
    }

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(pii_detection_llm_as_a_judge)
