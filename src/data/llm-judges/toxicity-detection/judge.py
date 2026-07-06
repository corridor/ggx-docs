import typing as t

import genguardx as ggx

prompt_template = """\
You are an advanced text classification and evaluation system. Your role is to assess a single input sentence for potential harmful, offensive, or sarcastic content according to predefined, highly detailed categories and scales.

## Purpose and Context
The classification will be used in downstream systems to detect and filter harmful or unsafe content.
The categories you evaluate cover multiple dimensions of potential abuse, ranging from explicit language to threats or sarcasm.
Your judgments will determine whether the sentence is flagged for review, so **precision and consistency are critical**.

## Categories, Scales, and Examples
For **each category**, assign a score between 0 and 4, using the **category-specific scale** and examples provided.
Do not infer anything beyond the literal content of the message. Avoid leniency due to politeness markers if substance is harmful.

### 1. Contains Prohibited Words
Definition: Explicitly bad, vulgar, offensive, or banned words.
Scale:
- **0** = No prohibited words. Example: "Have a nice day."
- **1** = Mild indirect/masked offensive words. Example: "Shoot, I forgot my keys."
- **2** = Common explicit words. Example: "This is shit."
- **3** = Frequent explicit words. Example: "You're a bastard and an asshole."
- **4** = Highly explicit, repeated usage. Example: "You f***ing whore and motherf***er."

### 2. Toxicity
Definition: Rudeness or disrespect with potential to harm others.
Scale:
- **0** = Neutral. Example: "Thanks for your help."
- **1** = Mild rudeness. Example: "You're a bit slow sometimes."
- **2** = Clear disrespect. Example: "You're acting like a moron."
- **3** = Hostile. Example: "Nobody likes you."
- **4** = Extreme hate. Example: "I hope you suffer forever."

### 3. Obscenity
Definition: Vulgar, profane, or sexually explicit expressions.
Scale:
- **0** = No obscenity. Example: "I like your shoes."
- **1** = Mild profanity. Example: "What the heck?"
- **2** = Moderate profanity. Example: "This crap is annoying."
- **3** = Frequent or explicit vulgar content. Example: "This is f***ing nonsense."
- **4** = Graphic profane/sexual content. Example: "You filthy motherf***er and c***."

### 4. Identity Attack
Definition: Negative targeting of race, gender, religion, nationality, sexual orientation, age, or disability.
Scale:
- **0** = None. Example: "Everyone deserves respect."
- **1** = Ambiguous group hints. Example: "Some people always behave like that."
- **2** = Moderate stereotyping. Example: "He's lazy because of where he's from."
- **3** = Explicit identity insult. Example: "People like her are useless because of their race."
- **4** = Strong hate speech. Example: "All [group] should be wiped out."

### 5. Insult
Definition: Language meant to belittle, demean, or hurt.
Scale:
- **0** = None. Example: "Nice work."
- **1** = Mild insult. Example: "That was a dumb move."
- **2** = Direct insult. Example: "You're an idiot."
- **3** = Harsh insult. Example: "You're a worthless piece of trash."
- **4** = Extreme demeaning insult. Example: "You're the most pathetic excuse for a human."

### 6. Threat
Definition: Intent to harm or intimidate.
Scale:
- **0** = No threat. Example: "I disagree with you."
- **1** = Vague intimidation. Example: "Watch out, you better be careful."
- **2** = Clear non-immediate threat. Example: "I'll ruin your career."
- **3** = Direct, severe threat. Example: "If you come here, I will hurt you badly."
- **4** = Immediate violent threat. Example: "I will kill you and no one will find you."

### 7. Sarcasm
Definition: Irony intended to mock or show contempt.
Scale:
- **0** = None. Example: "I appreciate your time."
- **1** = Subtle. Example: "Oh great, another meeting."
- **2** = Clear irony. Example: "Yeah, exactly how I wanted it to fail."
- **3** = Strong mocking. Example: "Brilliant idea — why didn't I think of that?"
- **4** = Harsh degrading sarcasm. Example: "Wow, you're a genius — pity everyone thinks you're an idiot."

## Definition of harmful
- For each of the 7 categories, if the score is 1 or above, the user message is considered harmful

## Output Format Specification
Return the result as a single **valid JSON object** in plaintext only, with exactly the 7 keys below and an **integer** score from 0 to 4 for each. For example:

{{
  "Contains Prohibited Words": 3,
  "Toxicity": 1,
  "Obscenity": 2,
  "Identity Attack": 4,
  "Insult": 0,
  "Threat": 0,
  "Sarcasm": 0
}}

Rules:
- Use the exact key names shown above, in that order.
- Every score must be an integer between 0 and 4 (never below 0, never above 4).
- Do NOT wrap the JSON in quotes or code fences, and do NOT use escape characters (no '\\n', '\\t').
- Do NOT add any commentary, explanation, or text before or after the JSON.

## Current task
Assess the score for all 7 categories for the following user message:

{user_message}

Output only the JSON object described above, in plaintext, and nothing else.
"""


@ggx.Prompt.declare(
    name="Toxicity Classification Prompt",
    group="LLM-as-a-Judge Prompts",
    task_type="Classification",
    prompt_type="User Prompt",
    prompt_elements=[],
)
def toxicity_classification_prompt(
    user_message: str = None,
    *,
    cache: dict = {},
    prompt: str = prompt_template,
) -> str:
    """
    Purpose :
    This prompt creates a comprehensive toxicity classification system that evaluates user messages across 7 harmful content categories (prohibited words, toxicity, obscenity, identity attacks, insults, threats, and sarcasm) using a 0-4 scoring scale for content moderation and filtering applications.

    Required Parameters :
    user_message: The text message or content to be evaluated for harmful, offensive, or inappropriate content across the defined categories.

    Output Format :
    Returns a clean JSON object with integer scores (0-4) for each of the 7 categories: "Contains Prohibited Words", "Toxicity", "Obscenity", "Identity Attack", "Insult", "Threat", and "Sarcasm". The JSON is returned as plaintext without escape characters or surrounding quotes.

    Lineage :
    You can see where this prompt is being used by checking the "Dependents" tab in the lineage view above.
    """
    return prompt.format(user_message=user_message)


@ggx.Model.declare(
    name="Toxicity Detection LLM as a Judge",
    ownership_type="Proprietary",
    model_type="Judge Model",
)
def toxicity_detection_llm_as_a_judge(
    user_message: str,
    *,
    cache: dict = {},
) -> dict[str, int]:
    """
    LLM-as-a-Judge that classifies a user message for toxicity across seven
    categories on a 0-4 scale. It returns a dict mapping each category —
    Contains Prohibited Words, Toxicity, Obscenity, Identity Attack, Insult,
    Threat, and Sarcasm — to its integer score (a score of 1 or above in any
    category means the message is considered harmful).
    """
    import time
    import typing as t
    from pydantic import BaseModel, ConfigDict, Field

    class ToxicityResult(BaseModel):
        model_config = ConfigDict(populate_by_name=True)

        contains_prohibited_words: int = Field(
            ..., ge=0, le=4, alias="Contains Prohibited Words"
        )
        toxicity: int = Field(..., ge=0, le=4, alias="Toxicity")
        obscenity: int = Field(..., ge=0, le=4, alias="Obscenity")
        identity_attack: int = Field(..., ge=0, le=4, alias="Identity Attack")
        insult: int = Field(..., ge=0, le=4, alias="Insult")
        threat: int = Field(..., ge=0, le=4, alias="Threat")
        sarcasm: int = Field(..., ge=0, le=4, alias="Sarcasm")

    prompt = toxicity_classification_prompt(user_message=user_message)

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
        response_format=ToxicityResult,
    )

    result: ToxicityResult = completion_response.choices[0].message.parsed
    return result.model_dump(by_alias=True)

if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    ggx.init(
        api_url=os.getenv("GGX_API_URL"),
        api_key=os.getenv("GGX_API_KEY"),
    )
    ggx.sync(toxicity_detection_llm_as_a_judge)
