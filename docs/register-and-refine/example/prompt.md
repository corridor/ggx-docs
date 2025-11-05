# Prompt Registration Guide

This guide covers how to register prompts on the Corridor platform, using an **Intent Classification Prompt** as a working example.

## What is a Prompt?

A prompt is a reusable instruction template that defines how an LLM should behave and respond. Prompts on Corridor can be:
- Versioned and tracked
- Combined with models in pipelines
- Tested and validated
- Shared across teams

---

## Registration Steps

### 1. Navigate to Prompt Registry

Go to **GenAI Studio → Prompt Registry** and click the **Create** button.

### 2. Fill in Basic Information

![alt text](image.png)

**Description:**

Write a clear description of what your prompt does.

**Example for Intent Classification:**
```
This prompt classifies customer card queries using a 5-step process. It handles 
5 card-related intents: ACTIVATE CARD, BLOCK CARD, CARD DETAILS, CHECK CARD ANNUAL 
FEE, and CHECK CURRENT BALANCE ON CARD.

The system handles typos, removes PII, and enforces single-intent selection. 
Outputs structured JSON for easy parsing.
```

**Group:** `Existing Customer Credit Card Related Prompts`

**Permissible Purpose:** Type or search for applicable purposes

**Task Type:** `Classification`

**Prompt Type:** `System Instruction`

**Prompt Elements:** Select elements used in your prompt (Persona + Goal, Tone, Task, Context, Examples, Reasoning Steps, Output Format, Constraints)

### 3. Configure Code Settings

![alt text](image-1.png)

**Alias:** `customer_intent_classification_prompt`
- A Python variable name to reference this prompt in pipelines

#### Prompt Template

The prompt template is where you write the actual instructions for the LLM. Use `{}` to reference argument variables.

**Example Prompt Template for Intent Classification:**
````markdown
# PERSONA & TONE
You are a trusted, efficient, and security-conscious digital assistant, 
specialized in handling banking-related queries for existing customers 
of BankX.

Maintain a tone that is:
- Professional: Clear, formal, and polite
- Concise: Direct answers without filler
- Data-driven: Never guess; respond only based on verified data
- English only

# GOAL
Accurately predict customer intent from a predefined list of possible intents.

# TASK INSTRUCTIONS:

### Step 1: Review Intent Definitions
Thoroughly understand the predefined list of intents.

### Step 2: Pre-Defined List of Intents

#### ACTIVATE CARD
- Definition: Request to activate a newly issued card
- Examples:
  • "How do I activate my new debit card?"
  • "Activate my credit card now."

#### BLOCK CARD
- Definition: Request to block lost, stolen, or compromised card
- Examples:
  • "Block my credit card immediately."
  • "I lost my debit card, can you block it?"

#### CARD DETAILS
- Definition: Inquiry about card information
- Examples:
  • "How many cards do I have?"
  • "What is the name on my card?"

#### CHECK CARD ANNUAL FEE
- Definition: Inquiry about annual fees
- Examples:
  • "What's the annual fee for my credit card?"
  • "How much is my card's yearly charge?"

#### CHECK CURRENT BALANCE ON CARD
- Definition: Inquiry about available balance
- Examples:
  • "What's my credit card balance?"
  • "How much money is on my debit card?"

### Step 3: Disambiguate and Summarize Customer Utterance
- Overlook grammatical/spelling errors
- Ignore PII (name, age, gender, personal data)
- Focus on main intention in long sentences

### Step 4: Mapping Query to Intent
- Map to most suitable intent from predefined list
- Ensure only one intent is chosen
- Recheck classification is in predefined list

### Step 5: Schema Compliance
OUTPUT FORMAT:
```json
{"classified_intent": "str"}
```

# EXAMPLE SCENARIOS:

Example 1:
    Input: "I need to activate my new credit card."
    
    REASONING STEPS:
    - Review intent definitions
    - Understand all available intents
    - No disambiguation needed (clear query)
    - Maps to "ACTIVATE CARD" intent
    - Output in JSON format
    
    Output:
```json
    {"classified_intent": "ACTIVATE CARD"}
```

# Customer Query 
Query: {customer_utterance}
````

#### Define Arguments

Arguments are inputs that get passed into the prompt template.

Click **+ Add Argument** to add:

| Alias | Type | Is Optional | Default Value |
|-------|------|-------------|---------------|
| `user_message` | String | ☐ No | - |

**Note:** Use `{customer_utterance}` in the template and map it from `user_message` in Prompt Creation Logic.

### 4. Add Resources & Inputs

![alt text](image-2.png)

If your prompt needs other registered objects (like persona prompts or helper functions), add them here.

**Example:**
- `credit_card_pipeline_persona_and_tone` - A separate prompt that defines the assistant's persona

### 5. Write Prompt Creation Logic (Optional)

The Prompt Creation Logic allows you to programmatically process arguments before inserting them into the template.

**Example - Formatting Intent Definitions:**

```python
intent_definitions = [
    {
        "Intent": "ACTIVATE CARD",
        "Definition": "Request to activate a newly issued card",
        "Examples": [
            "How do I activate my new debit card?",
            "Activate my credit card now.",
        ],
    },
    {
        "Intent": "BLOCK CARD",
        "Definition": "Request to block a lost, stolen, or compromised card",
        "Examples": [
            "Block my credit card immediately.",
            "I lost my debit card, can you block it?",
        ],
    },
    {
        "Intent": "CARD DETAILS",
        "Definition": "Inquiry about card information",
        "Examples": [
            "How many cards do I have?",
            "What is the name on my card?",
        ],
    },
    {
        "Intent": "CHECK CARD ANNUAL FEE",
        "Definition": "Inquiry about annual fees",
        "Examples": [
            "What's the annual fee for my credit card?",
            "How much is my card's yearly charge?",
        ],
    },
    {
        "Intent": "CHECK CURRENT BALANCE ON CARD",
        "Definition": "Inquiry about available balance",
        "Examples": [
            "What's my credit card balance?",
            "How much money is on my debit card?",
        ],
    },
]

def get_intent_info(data_list):
    """Format intent definitions into readable text"""
    formatted_list = []
    intent_number = 1
    
    for item in data_list:
        formatted_list.append(f"#### {intent_number}. {item['Intent'].upper()}")
        formatted_list.append(f"- Definition: {item['Definition']}")
        formatted_list.append(f"- Examples:")
        for example in item["Examples"]:
            formatted_list.append(f"  • {example}")
        formatted_list.append("")  # Empty line between intents
        intent_number += 1
    
    return "\n".join(formatted_list)

# Fill in the prompt template
return prompt.format(
    customer_utterance=user_message,
    list_of_intents=get_intent_info(intent_definitions)
)
```

**What This Does:**
1. Defines 5 card-related intent definitions with examples
2. Formats them into a structured, numbered list
3. Fills in `{customer_utterance}` and `{list_of_intents}` placeholders

### 6. Save the Prompt

Click **Create** to register the prompt.

The prompt is now:
- Available in the Prompt Registry
- Usable in pipelines and other objects

---

## Using Prompts in Pipelines

Once registered, prompts can be used in pipelines:

```python
# Reference the prompt in pipeline code
intent_result = customer_intent_classification_prompt(
    user_message=user_input
)

# Access the classified intent
classified_intent = intent_result["classified_intent"]

# Use in downstream logic
if classified_intent == "ACTIVATE CARD":
    # Handle card activation
    pass
elif classified_intent == "BLOCK CARD":
    # Handle card blocking
    pass
```

---

## Related Documentation

- [Model Registration Guide](../model/) - Register LLM models to use with prompts
- [Pipeline Registration Guide](../pipeline/) - Combine prompts with models in workflows
---

## Next Steps

After registering your prompt:

1. **Register a model** - If you haven't already, register the LLM to use with this prompt
2. **Build a pipeline** - Combine your prompt with a model and other resources

---

By following this guide, you can create well-structured, maintainable prompts that drive reliable LLM behavior across your organization.