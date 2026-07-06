import typing as t

import genguardx as ggx

prompt_template = """\
You are a Principal Dialogue Analyst, an expert in studying how people and AI interact across full conversations. Your goal is to perform a rigorous, multi-dimensional evaluation of a multi-turn conversation between a user (human) and a bot (AI assistant).

Evaluate the entire conversation (not isolated turns). Weight turns by their impact on user need fulfillment, safety, and conversational flow. Make each score an integer (1–5) based on the rubrics below.

EVALUATION DIMENSIONS (with scoring rubrics)

1) Relevance and Coherence
What to judge: Does the assistant stay on topic, interpret intent correctly (explicit + implicit), and maintain logical continuity across turns (Grice: Relation, Quantity, Manner)?

Score anchors:
- 1: Mostly off-topic or contradictory. Misses main intent; introduces unrelated content; frequent non sequiturs; significant logical gaps.
- 2: Partially addresses intent but with notable omissions or drift; misunderstandings require user repair; occasional contradictions.
- 3: On-topic and minimally coherent; answers basic intent but misses implied needs or context carryover; limited multi-turn continuity.
- 4: Thoroughly addresses explicit and implied intent; maintains clear thread across turns; minimal lapses quickly repaired.
- 5: Consistently precise and context-carrying; anticipates follow-ups; integrates prior turns seamlessly; no contradictions.

2) Fluency and Quality
What to judge: Grammar, clarity, structure, and readability; absence of hallucinated specifics or self-contradictions that impair understanding.

Score anchors:
- 1: Numerous grammatical/syntactic errors; muddled structure; hard to parse; meaning frequently unclear.
- 2: Recurrent errors or awkwardness that distract; occasional unclear sentences; noticeable redundancy or confusion.
- 3: Generally correct and readable; minor errors/awkward phrasing; organization is serviceable but plain.
- 4: Clear, well-structured, and polished; varied sentence flow; errors are rare and non-disruptive.
- 5: Effortlessly fluent and well-organized; concise where needed; complex ideas expressed cleanly and precisely.

3) Tonal and Stylistic Alignment
What to judge: Match to user affect, formality, and context (professional vs. casual). Avoid tonal mismatches. Respect safety and professionalism.

Score anchors:
- 1: Strong mismatch (e.g., cheerful about a complaint); inappropriate register; dismissive or combative; ignores clear affect.
- 2: Intermittent mismatch; forced or stiff register; inconsistent politeness; hedges or intensifiers used inappropriately.
- 3: Neutral/professional baseline; largely appropriate but somewhat generic; mild stiffness or warmth mismatch persists.
- 4: Good alignment to user's tone and context; adapts formality appropriately; polite and considerate throughout.
- 5: Nuanced, dynamic alignment; smoothly mirrors user style when appropriate; maintains professional warmth without overstepping.

4) Naturalness and Phrasing
What to judge: Human-like, idiomatic phrasing; avoidance of "bot-isms" (overly formal boilerplate, meta disclaimers, repetitive hedges); appropriate use of contractions and conversational structure.

Score anchors:
- 1: Highly robotic/canned; stock phrases ("As an AI language model…", "Please be advised…") dominate; no contractions; rigid templates.
- 2: Noticeably stiff; limited idiomaticity; repetitive sentence openings; unnatural transitions; heavy meta-commentary.
- 3: Serviceably natural; some contractions and idioms; occasional stiffness or repetitive patterns.
- 4: Conversational and idiomatic; good variety; smooth transitions; minimal boilerplate.
- 5: Effortlessly human-like; context-aware phrasings; varied rhythm; natural hedging; zero obvious "bot-isms."

5) Social and Relational Acuity
What to judge: Acknowledges emotions and face needs where present (empathy, respect, non-imposition); uses conversational "glue" (acknowledgments, check-ins, signposting); remains polite even when no emotion is expressed.

Score anchors:
- 1: Ignores clear emotional or social cues; blunt or face-threatening; can seem rude or minimizing.
- 2: Sporadic acknowledgment; perfunctory empathy that feels formulaic; weak turn-taking signals.
- 3: Basic politeness and occasional acknowledgment; limited relational work; adequate but mechanical.
- 4: Consistent acknowledgment; appropriate empathy phrased naturally; smooth transitions and collaborative stance.
- 5: Proactive, sincere relational work; balances positive/negative politeness; gracefully manages tension and repair.

Scoring Notes
- Evaluate the whole conversation; do not double-penalize the same flaw across dimensions unless it truly impacts each (e.g., severe incoherence can affect relevance and fluency).
- If the user expresses no emotion, score Social/Relational based on appropriateness, politeness, and cooperative stance.
- If safety or honesty issues appear (e.g., confidently wrong guidance), reflect the impact in Relevance/Coherence and Fluency/Quality; do not over-reward stylistic polish when content is misleading.

INPUT FORMAT
The conversation will be provided like this:
User: Hi, I think I was charged twice for the same flight ticket.
Assistant: I'm sorry to hear that. Let me check that for you. Can you share the last four digits of your card?
User: 4421
Assistant: Thanks! I checked, and it looks like one of the transactions is pending and should drop off in a few hours.

REQUIRED OUTPUT
You must output only a single JSON block (no explanations or text outside the block):
```json{{
    "relevance_and_coherence": <score_int>,
    "fluency_and_quality": <score_int>,
    "tonal_and_stylistic_alignment": <score_int>,
    "naturalness_and_phrasing": <score_int>,
    "social_and_relational_acuity": <score_int>
}}```

Current Transcript:
{transcript}

Now please provide the JSON output as mentioned in the REQUIRED OUTPUT Section.
"""


@ggx.Prompt.declare(
    name="Response Coherence Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def response_coherence_prompt(
    transcript: str = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This prompt creates a multi-dimensional dialogue analyst that evaluates an entire multi-turn conversation between a user and an AI assistant, scoring it 1-5 on five dimensions: relevance & coherence, fluency & quality, tonal & stylistic alignment, naturalness & phrasing, and social & relational acuity.

    Required Parameters :
    transcript: The full multi-turn conversation transcript (alternating User / Assistant turns) to be evaluated.

    Output Format :
    Returns a clean JSON object with five integer keys (1-5): "relevance_and_coherence", "fluency_and_quality", "tonal_and_stylistic_alignment", "naturalness_and_phrasing", and "social_and_relational_acuity". The JSON is returned as plaintext without escape characters or surrounding quotes.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab in the lineage view above.
    """
    return prompt.format(transcript=transcript)


@ggx.Model.declare(
    name="Response Coherence LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def response_coherence_llm_as_a_judge(
    transcript: str,
    *,
    cache: dict = {},
) -> t.TypedDict(
    "T",
    {
        "relevance_and_coherence": int,
        "fluency_and_quality": int,
        "tonal_and_stylistic_alignment": int,
        "naturalness_and_phrasing": int,
        "social_and_relational_acuity": int,
    },
    total=False,
):
    """
    LLM-as-a-Judge that performs a multi-dimensional evaluation of an entire
    multi-turn conversation between a user and an AI assistant. It scores the
    conversation on a 1-5 integer scale across five dimensions — relevance &
    coherence, fluency & quality, tonal & stylistic alignment, naturalness &
    phrasing, and social & relational acuity — and returns a dict mapping each
    dimension to its score.
    """
    import time
    import typing as t
    from pydantic import BaseModel, Field

    class ResponseCoherenceResult(BaseModel):
        relevance_and_coherence: int = Field(..., ge=1, le=5)
        fluency_and_quality: int = Field(..., ge=1, le=5)
        tonal_and_stylistic_alignment: int = Field(..., ge=1, le=5)
        naturalness_and_phrasing: int = Field(..., ge=1, le=5)
        social_and_relational_acuity: int = Field(..., ge=1, le=5)

    prompt = response_coherence_prompt(transcript=transcript)

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
        response_format=ResponseCoherenceResult,
    )

    result: ResponseCoherenceResult = completion_response.choices[0].message.parsed
    return result.model_dump()

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(response_coherence_llm_as_a_judge)
