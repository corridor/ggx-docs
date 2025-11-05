# Pipeline Registration Guide

This guide covers how to register pipelines on the Corridor platform, using an **Intent Classification Pipeline** as a working example.

## Prerequisites

Before registering a pipeline, ensure you have:
- ✅ **Registered a Model** - Follow the [Model Registration Guide](../model/) to register Gemini 2.0 Flash
- ✅ **Registered a Prompt** - Follow the [Prompt Registration Guide](../prompt/) to register the intent classification prompt

If you haven't completed these steps, please do so before proceeding.

---

## What is a Pipeline?

A pipeline combines multiple resources (models, prompts, RAGs, helper functions) to create an end-to-end workflow. Pipelines on Corridor can be:
- Chat-based (maintain conversation history) or Free-flow (single input/output)
- Versioned and tracked
- Tested and validated
- Monitored in production

---

## Registration Steps

### 1. Navigate to Pipeline Registry

Go to **GenAI Studio → Pipeline Registry** and click the **Create** button.

### 2. Fill in Basic Information

![alt text](image-3.png)

**Description:**

Write a clear description of what your pipeline does.

**Example for Intent Classification Pipeline:**
```
This is a chat-based pipeline designed for intent recognition & classifies incoming user 
messages by assigning them to one of the following predefined intents:

1. ACTIVATE CARD
2. APPLY FOR LOAN
3. APPLY FOR MORTGAGE
4. BLOCK CARD
5. CANCEL LOAN

This pipeline operates on a single input and produces a single output for each message, 
without maintaining conversational context across interactions.
```

**Group:** `Conversational AI ChatBot Pipeline (credit-card)`

**Permissible Purpose:** Type or search for applicable purposes

**Task Type:** `Question-Answering`

**Data Usage:** `No Additional Data`

**Internal-Only:** Check if pipeline should not be exposed externally

**`Conversational AI ChatBot Pipeline (credit-card) Scenarios:** Select applicable scenarios

### 3. Configure Code Settings

![alt text](image-4.png)

**Alias:** `customer_intent_classification_pipeline`
- A Python variable name to reference this pipeline

**Input Type:** `Python Function`
- Choose between Python Function or External Agent

**Pipeline Type:** `Chat Based Pipeline`
- Chat Based: Maintains conversation history
- Free Flow: Single input/output without context

**Context Type:** `String`
- The data type for conversation context

**Interaction Type:** `Struct[role: String, content: String]`
- Format for chat messages

#### Add Resources

Click **+ Create New** or search for existing resources:

**LLMs / Models:**
- `gemini_2_0_flash` - The foundation model we registered earlier

**Prompts:**
- `customer_intent_classification_prompt` - The intent classification prompt we registered earlier

These are the model and prompt you registered in the previous guides.

### 4. Write Pipeline Scoring Logic

![alt text](image-5.png)

The scoring logic defines how the pipeline processes inputs and generates outputs.

**Example - Intent Classification Pipeline:**

```python
import json

# Run Gemini with prompt and user input
response = gemini_2_0_flash(
    customer_intent_classification_prompt(user_message=user_message)
)

# Parse the JSON response to get the classified intent
response_json = json.loads(response["response"])
classified_intent = response_json.get("classified_intent", "UNKNOWN")

# List of valid intents
valid_intents = [
    "ACTIVATE CARD",
    "BLOCK CARD",
    "CARD DETAILS",
    "CHECK CARD ANNUAL FEE",
    "CHECK CURRENT BALANCE ON CARD",
]

# Validate the classified intent
if classified_intent not in valid_intents:
    classified_intent = "UNKNOWN"

# Return output and context
return {
    "output": f"Classified as: {classified_intent}",
    "context": classified_intent
}
```

**What This Does:**
1. Calls the Gemini model with the classification prompt and user message
2. Parses the JSON response to extract the classified intent
3. Validates the intent against the list of valid intents
4. Returns the classification result and stores it in context

**Variables Available:**
- `user_message` - The current user input (type: String)
- `history` - Previous conversation messages (type: Array[Struct])
- `context` - Data from previous turns (type: String)

### 5. Add Examples (Optional)

![alt text](image-6.png)

Add test examples to validate pipeline behavior:

| Initial User Message | Context | Expected Output |
|---------------------|---------|-----------------|
| I want to activate my card. | Arizona | Classified as: ACTIVATE CARD |
| Want to check my recent transactions. | Arizona | Classified as: CHECK RECENT TRANSACTIONS |
| How to change my password? | Arizona | Classified as: SET UP PASSWORD |
| Tell me a joke. | Arizona | Classified as: OUT OF CONTEXT |

**Note:** Examples help with testing and documenting expected behavior.

### 6. Save the Pipeline

Click **Create** to register the pipeline.

The pipeline is now:
- Available in the Pipeline Registry
- Ready for simulation and testing

---

## Pipeline Types

### Chat Based Pipeline
- Maintains conversation history across turns
- Has access to `history` and `context` variables
- Suitable for: Chatbots, and multi-turn conversations

### Free Flow Pipeline
- Processes one input at a time
- No conversation history
- Suitable for: Single-shot classification, and one-off predictions

---

## Testing Your Pipeline

After creating the pipeline, you can test it in two ways:

### 1. Test via Chat Interface
- Go to the top right corner of the pipeline page
- Click **Run** → **Chat Session**
- Enter sample user messages and verify the outputs

### 2. Test Code During Creation/Editing
- While creating or editing the pipeline (click **Edit** button next to **Run**)
- Scroll to the Code section
- Click the **Test Code** button in the bottom right corner of the Code section
- This allows you to test the pipeline logic directly without saving

---

## Using Pipelines

### In Applications

Reference the pipeline in your application code:

```python
# Call the pipeline
result = customer_intent_classification_pipeline(
    user_message="I want to block my card",
    history=[],
    context=""
)

# Access the output
output = result["output"]  # "Classified as: BLOCK CARD"
intent = result["context"]  # "BLOCK CARD"
```

---

## Related Documentation

- [Model Registration Guide](../model/) - Register foundation models
- [Prompt Registration Guide](../prompt/) - Create reusable prompts

---

By following this guide, you can create reliable, production-ready pipelines that combine multiple AI resources into cohesive workflows.