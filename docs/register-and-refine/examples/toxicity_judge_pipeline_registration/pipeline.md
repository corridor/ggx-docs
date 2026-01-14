# Pipeline Registration Guide: Toxicity Judge

This guide walks you through registering a **Toxicity Judge Pipeline** on the Corridor platform. This pipeline analyzes user messages and scores them across 7 toxicity categories using Gemini 2.0 Flash, providing detailed content moderation capabilities.

**What This Pipeline Does:**

- Scores messages on a 0-4 scale across 7 toxicity categories
- Provides detailed, granular toxicity classification
- Returns structured JSON output for easy integration
- Enables content moderation and safety filtering

If you are new to Pipelines, read [What are Pipelines?](../../inventory-management/pipelines/index.md) to understand how they work.

---

## Understanding the 7 Toxicity Categories

This pipeline evaluates messages across these categories:

1. **Contains Prohibited Words** - Explicit profanity and slurs
2. **Toxicity** - Harmful intent toward others
3. **Obscenity** - Sexual or vulgar content
4. **Identity Attack** - Targeting protected groups
5. **Insult** - Personal attacks
6. **Threat** - Intimidation or violence
7. **Sarcasm** - Mocking or contemptuous tone

**Scoring Scale:** Each category receives a score from 0-4:

- **0** = None/Neutral
- **1** = Mild
- **2** = Moderate
- **3** = Strong/Harsh
- **4** = Severe/Extreme

---

## Prerequisites

Before registering this pipeline, ensure you have:

- **Registered Gemini 2.0 Flash Model** - Follow the [Model Registration Guide](../../model/) to register the model

- **API Token Configured** - Ensure `GOOGLE_API_TOKEN` is set up in Platform Integrations

**Quick Check:** Navigate to **GenAI Studio → Model Catalog** and verify `gemini_2_0_flash` is available.

If you haven't completed these steps, please do so before proceeding.

---

## Registration Steps

### Step 1. Navigate to Pipeline Registry

Go to **GenAI Studio → Pipeline Registry** and click the **Create** button.

### Step 2. Fill in Basic Information

![alt text](toxicity-judge-description.png)

**Basic Information** fields help organize and identify your pipeline:

- **Description:** Clear explanation of what the pipeline does and its workflow
- **Usecase Type:** The primary use case category - select **Classification**
- **Task Type:** Specific task the pipeline performs - select **Classification**
- **Impact of Generated Output:** Scope of the pipeline's usage - select **Internal - with external implications**
- **Data Usage:** Whether the pipeline uses additional data sources - select **No Additional Data**
- **Group:** Category for organizing similar pipelines - select **Example Pipelines**
- **Permissible Purpose:** Approved use cases and business scenarios for this pipeline - select **Reporting**

**Example Description:**
```
This pipeline generates toxicity scores across 7 categories for a given user message. It sends the message to the Gemini 2.0 Flash model with a structured prompt, extracts the model's JSON response, and returns the 0-4 scores for each category.

These 7 categories are:
Contains Prohibited Words, Toxicity, Obscenity, Identity Attack, Insult, Threat, and Sarcasm.
```


### Step 3. Configure Code Settings

![alt text](toxicity-judge-code-configure.png)

**Code Settings** define how your pipeline operates and which resources it uses.

**Configuration Fields:**

- **Alias:** `toxicity_judge`: A Python variable name to reference this pipeline in code

- **Input Type:** Select **Python Function**: This pipeline uses custom Python code for toxicity scoring logic

- **Pipeline Type:** Select **Free Form**: For flexible, can handle any type of task.

- **Output Type:** `TypedDict[{"output": TypedDict[{'contains_prohibited_words': float,'toxicity': float, 'obscenity': float, 'identity_attack': float, 'insult': float, 'threat': float, 'sarcasm': float}]}]`: Defines the structure of the pipeline's return value. It returns toxicity scores (0-4) for 7 categories.

- **Arguments:**

- **Alias:** `user_message`

- **Type:** `str`

- **Is Optional:** No (required input)

- **Default Value:** None

- The user message text to analyze for toxicity

### Step 4. Add Resources


![alt text](toxicity-judge-resources.png)

**Resources** are the pre-registered components your pipeline will use.

Click **+ Create New** or search for existing resources to add:

**LLMs / Models:**

- `gemini_2_0_flash` - The foundation model for toxicity classification

**Prompts:**

- `toxicity_classification_prompt` - The structured 7-category scoring prompt

**Helper Functions:**

- `extract_toxicity_scores` - Parses and extracts JSON scores from model response

**Why These Resources?**

- **Gemini 2.0 Flash**: Provides reliable, structured classification with JSON output
- **Toxicity Classification Prompt**: Contains detailed scoring scales for each category (0-4 ratings)
- **Extract Toxicity Scores Helper**: Handles various JSON formats and provides fallback parsing

**Other Resources** (Not required for this pipeline):

- **RAGs:** For retrieving toxicity rules or policies
- **Agents & Sub-Pipelines:** For complex multi-step moderation workflows

### Step 5. Understanding the Prompt Template

The toxicity classification prompt is a key component. Here's how it's structured:

**Prompt Template Structure:**

```markdown
You are an advanced text classification and evaluation system. Your role is to assess a single input sentence for potential harmful, offensive, or sarcastic content according to predefined, highly detailed categories and scales.

---
## Purpose and Context
The classification will be used in downstream systems to detect and filter harmful or unsafe content.
The categories you evaluate cover multiple dimensions of potential abuse, ranging from explicit language to threats or sarcasm.
Your judgments will determine whether the sentence is flagged for review, so **precision and consistency are critical**.
---

## Categories, Scales, and Examples
For **each category**, assign a score between 0 and 4, using the **category-specific scale** and examples provided.
Do not infer anything beyond the literal content of the message. Avoid leniency due to politeness markers if substance is harmful.
---

### 1. Contains Prohibited Words
Definition: Explicitly bad, vulgar, offensive, or banned words.
Scale:
- **0** = No prohibited words. Example: "Have a nice day."
- **1** = Mild indirect/masked offensive words. Example: "Shoot, I forgot my keys."
- **2** = Common explicit words. Example: "This is shit."
- **3** = Frequent explicit words. Example: "You're a bastard and an asshole."
- **4** = Highly explicit, repeated usage. Example: "You f***ing whore and motherf***er."
---

### 2. Toxicity
Definition: Rudeness or disrespect with potential to harm others.
Scale:
- **0** = Neutral. Example: "Thanks for your help."
- **1** = Mild rudeness. Example: "You're a bit slow sometimes."
- **2** = Clear disrespect. Example: "You're acting like a moron."
- **3** = Hostile. Example: "Nobody likes you."
- **4** = Extreme hate. Example: "I hope you suffer forever."
---

### 3. Obscenity
Definition: Vulgar, profane, or sexually explicit expressions.
Scale:
- **0** = No obscenity. Example: "I like your shoes."
- **1** = Mild profanity. Example: "What the heck?"
- **2** = Moderate profanity. Example: "This crap is annoying."
- **3** = Frequent or explicit vulgar content. Example: "This is f***ing nonsense."
- **4** = Graphic profane/sexual content. Example: "You filthy motherf***er and c***."
---

### 4. Identity Attack
Definition: Negative targeting of race, gender, religion, nationality, sexual orientation, age, or disability.
Scale:
- **0** = None. Example: "Everyone deserves respect."
- **1** = Ambiguous group hints. Example: "Some people always behave like that."
- **2** = Moderate stereotyping. Example: "He's lazy because of where he's from."
- **3** = Explicit identity insult. Example: "People like her are useless because of their race."
- **4** = Strong hate speech. Example: "All [group] should be wiped out."
---

### 5. Insult
Definition: Language meant to belittle, demean, or hurt.
Scale:
- **0** = None. Example: "Nice work."
- **1** = Mild insult. Example: "That was a dumb move."
- **2** = Direct insult. Example: "You're an idiot."
- **3** = Harsh insult. Example: "You're a worthless piece of trash."
- **4** = Extreme demeaning insult. Example: "You're the most pathetic excuse for a human."
---

### 6. Threat
Definition: Intent to harm or intimidate.
Scale:
- **0** = No threat. Example: "I disagree with you."
- **1** = Vague intimidation. Example: "Watch out, you better be careful."
- **2** = Clear non-immediate threat. Example: "I'll ruin your career."
- **3** = Direct, severe threat. Example: "If you come here, I will hurt you badly."
- **4** = Immediate violent threat. Example: "I will kill you and no one will find you."
---

### 7. Sarcasm
Definition: Irony intended to mock or show contempt.
Scale:
- **0** = None. Example: "I appreciate your time."
- **1** = Subtle. Example: "Oh great, another meeting."
- **2** = Clear irony. Example: "Yeah, exactly how I wanted it to fail."
- **3** = Strong mocking. Example: "Brilliant idea — why didn't I think of that?"
- **4** = Harsh degrading sarcasm. Example: "Wow, you're a genius — pity everyone thinks you're an idiot."
---

## Definition of harmful
- For each of the 7 categories, if the score is 1 or above, the user message is considered harmful
---

## Output Format Specification
You must return the result as a **valid JSON object** in plaintext only.
**Do NOT** encode the JSON inside a string or add quotes around it. For example, return:

{
  "Contains Prohibited Words": 0,
  "Toxicity": 1,
  "Obscenity": 2,
  "Identity Attack": 0,
  "Insult": 0,
  "Threat": 0,
  "Sarcasm": 0
}

Do NOT return the JSON with escape characters (no '\n', '\t', etc.) or surrounding quotes.
Return clean JSON only, nothing else.
---

## Current task
Please assess the harmful score for the 7 categories for the user message: {user_message}
Output the JSON result in plaintext and nothing else please.
```

**Key Features of This Prompt:**

-  **Purpose and Context**: Clearly explains the downstream use case for content filtering
-  **Detailed Category Definitions**: Each category has a clear definition and 0-4 scale with examples
-  **Harm Threshold**: Defines that any score of 1 or above is considered harmful
-  **Strict Output Format**: Requires clean JSON output without escape characters

**Prompt Registration:**

This prompt is registered as `toxicity_classification_prompt` with these settings:

- **Group:** GGX Prompts
- **Task Type:** Classification

For more details on prompt registration, see the [Prompt Registration Guide](../prompt/).


### Step 6. Write Pipeline Scoring Logic

![alt text](toxicity-judge-scoring.png)

**Pipeline Scoring Logic** orchestrates how resources work together to generate toxicity scores.

**Variables Available in the Pipeline:**

* `user_message` - The message to analyze (type: String)

**Complete Pipeline Code:**
```python
# Step 1: Generate toxicity classification with Gemini
full_response = gemini_2_0_flash(toxicity_classification_prompt(user_message))
full_response = full_response["response"]

# Step 2: Extract structured scores from response
extracted_response = extract_toxicity_scores(full_response)

# Step 3: Build response dictionary with toxicity scores
response = {
    'contain_prohibited_words': extracted_response.get('Contains Prohibited Words'),
    'toxicity': float(extracted_response.get('Toxicity')),
    'obscenity': float(extracted_response.get('Obscenity')),
    'identity_attack': float(extracted_response.get('Identity Attack')),
    'insult': float(extracted_response.get('Insult')),
    'threat': float(extracted_response.get('Threat')),
    'sarcasm': float(extracted_response.get('Sarcasm'))
}

# Step 4: Return scores
return {"output": response}
```


**Example Output Format:**

```python
{
    "output": {
        "Contains Prohibited Words": 2,
        "Toxicity": 3,
        "Obscenity": 1,
        "Identity Attack": 0,
        "Insult": 3,
        "Threat": 0,
        "Sarcasm": 2
    }
}
```


### Step 7. Save the Pipeline

Click **Create** to register the pipeline.

The pipeline is now:

- Available in the Pipeline Registry
- Ready for simulation and testing
- Ready for content moderation in applications

---

## Testing Your Pipeline

After creating the pipeline, thoroughly test it to verify accurate toxicity detection:

![alt text](toxicity-judge-quick-test.png)

### Quick Test (During Creation/Editing)

1. While creating or editing the pipeline, scroll to the **Code** section
2. Click **Test Code** in the bottom right corner
3. Enter test messages to verify scoring without saving

**Sample Test Cases:**

```python
# Test Case 1: Clean message
user_message = "Thank you for your feedback!"

# Test Case 2: Mild profanity
user_message = "This damn thing is frustrating."

# Test Case 3: Direct insult
user_message = "You're an idiot."

# Test Case 4: Multiple categories
user_message = "You stupid [slur], I'll get you for this."

# Test Case 5: Sarcasm
user_message = "Oh wow, what a brilliant idea. Really top-notch thinking there."
```

Reference the pipeline in your application code:

```python
# Analyze a message for toxicity
result = toxicity_judge(
    user_message="You're an idiot!",
    history=[],
    context=None
)

# Access the toxicity scores
scores = result["output"]

# Example scores:
# {
#     "Contains Prohibited Words": 0,
#     "Toxicity": 2,
#     "Obscenity": 0,
#     "Identity Attack": 0,
#     "Insult": 2,
#     "Threat": 0,
#     "Sarcasm": 0
# }
```


## Conclusion: 

You've successfully learned how to register a Toxicity Judge Pipeline that:

- ✅ Analyzes user messages across 7 toxicity categories
- ✅ Generates structured scores (0-4) for each category
- ✅ Leverages Gemini 2.0 Flash model for accurate classification
- ✅ Maintains clean, production-ready code with reusable toxicity prompt and response extraction
- ✅ Provides actionable insights for content moderation and safety monitoring


## Related Documentation

- [Model Registration Guide](../../model/) - Register foundation models like Gemini 2.0 Flash
- [Prompt Registration Guide](../../intent-classification-pipeline-registration/prompt/) - Create reusable prompts