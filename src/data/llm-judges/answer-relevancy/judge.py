import typing as t

import genguardx as ggx

prompt_template = """\
You are an expert evaluation system specialized in measuring **Answer Relevancy**.

Your role is to judge how relevant a given RESPONSE is to a given USER MESSAGE, and to assign a single integer score from 0 to 4.

## What "Answer Relevancy" Means
Answer relevancy measures whether the response directly and appropriately addresses what the user actually asked or requested. It is concerned ONLY with relevance — NOT with factual correctness, grammar, writing style, tone, or safety on their own.

A relevant answer:
- Directly addresses the user's question, request, or underlying intent.
- Stays on topic and focuses on what was asked.
- Covers the core of what the user is looking for.
- Does not bury the answer under large amounts of unrelated, off-topic, or filler content.

## Generality (works across many answer types)
This metric is intentionally generic and MUST work across many types of exchanges, including but not limited to:
- Factual / informational questions ("What is X?")
- How-to / procedural requests ("How do I do X?")
- Open-ended or opinion questions ("What do you think about X?")
- Multi-part questions (each part should be addressed)
- Task / instruction following ("Summarize this", "Write code that ...", "Translate ...")
- Conversational or clarifying exchanges

## Judging Principles
- Judge relevance to the user's INTENT, not just surface keyword overlap.
- A factually wrong but on-topic answer can still be relevant — do NOT penalize factual errors here, only relevance.
- A fluent, correct-sounding, but off-topic answer is NOT relevant.
- If the user asks multiple things, only partially answering reduces relevance.
- A refusal, clarifying question, or "I don't know" is relevant ONLY when that is an appropriate response to the request; an evasive non-answer to a clearly answerable question is low relevance.
- Excessive irrelevant padding around an otherwise correct answer reduces relevance.

## Scoring Scale (0 to 4)
Assign exactly one integer score:

- **0 — Completely irrelevant**: Does not address the user message at all. Off-topic, empty, or answers a different question.
  Example — User: "What's the capital of France?" Response: "I enjoy hiking on weekends."

- **1 — Mostly irrelevant**: Touches the general topic but fails to address the actual question or intent; dominated by off-topic content.
  Example — User: "How do I reset my password?" Response: "Passwords are important and you should change them often."

- **2 — Partially relevant**: Addresses some of the request but misses key parts, is notably incomplete, or mixes in substantial irrelevant content.
  Example — User: "List 3 benefits of exercise and explain each." Response: "Exercise is good for your heart." (only one benefit, no explanation of the rest)

- **3 — Mostly relevant**: Directly addresses the user's intent with only minor gaps, slight off-topic drift, or small amounts of extraneous content.
  Example — User: "How do I reset my password?" Response: gives the correct steps but adds an unnecessary tangent.

- **4 — Fully relevant**: Directly, completely, and precisely addresses the user's message and intent, with no meaningful irrelevant content. All parts of a multi-part request are covered.
  Example — User: "What's the capital of France?" Response: "The capital of France is Paris."

## Output Format Specification
Return the result as a single **valid JSON object** in plaintext only, with exactly these two keys:

{{
  "score": one integer between 0 and 4,
  "reasoning": "Concise justification (1-2 sentences) explaining the score by referencing how well the response addresses the user message."
}}

Rules:
- "score" MUST be an integer between 0 and 4 (never a float, never below 0, never above 4).
- "reasoning" MUST be a concise string explaining the score.
- Do NOT wrap the JSON in quotes or code fences, and do NOT use escape characters (no '\\n', '\\t').
- Do NOT add any commentary, explanation, or text before or after the JSON object.

## Current task
Evaluate the answer relevancy of the RESPONSE with respect to the USER MESSAGE.

### USER MESSAGE:
{user_message}

### RESPONSE:
{response}

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="Answer Relevancy Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def answer_relevancy_prompt(
    user_message: str = None,
    response: str = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This prompt creates a generic answer-relevancy evaluation system that, given a user message and a response, judges how well the response addresses the user's question or intent on a 0-4 scale. It is intentionally domain-agnostic so it can be applied to factual questions, how-to requests, open-ended questions, multi-part questions, and instruction-following tasks.

    Required Parameters :
    user_message: The original question, request, or instruction from the user.
    response: The answer/output being evaluated for relevancy against the user message.

    Output Format :
    Returns a clean JSON object with two keys: an integer "score" (0-4) and a string "reasoning" justifying the score. The JSON is returned as plaintext without escape characters or surrounding quotes.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab in the lineage view above.
    """
    return prompt.format(user_message=user_message, response=response)


@ggx.Model.declare(
    name="Answer Relevancy LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def answer_relevancy_llm_as_a_judge(
    user_message: str,
    response: str,
    *,
    cache: dict = {},
) -> t.TypedDict("T", {"score": int, "reasoning": str}, total=False):
    """
    LLM-as-a-Judge that measures answer relevancy: given a user message and a
    response, it scores how well the response addresses the user's question or
    intent on a 0-4 scale (0 = completely irrelevant, 4 = fully relevant) and
    returns a dict with an integer "score" and a string "reasoning".

    The judge is intentionally generic and works across many answer types
    (factual, how-to, open-ended, multi-part, and instruction-following).
    Relevancy is judged independently of factual correctness — an on-topic but
    factually wrong answer can still be relevant.
    """
    import time
    import typing as t
    from pydantic import BaseModel, Field

    class AnswerRelevancyResult(BaseModel):
        score: int = Field(
            ...,
            ge=0,
            le=4,
            description="Integer 0 (completely irrelevant) to 4 (fully relevant).",
        )
        reasoning: str = Field(
            ...,
            description="Concise 1-2 sentence justification for the score.",
        )

    prompt = answer_relevancy_prompt(user_message=user_message, response=response)

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
        response_format=AnswerRelevancyResult,
    )

    result: AnswerRelevancyResult = completion_response.choices[0].message.parsed
    return result.model_dump()

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(answer_relevancy_llm_as_a_judge)