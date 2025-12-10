# Pipeline Registration Guide

A pipeline combines multiple resources (models, prompts, RAGs, helper functions) to create an end-to-end use-case specific workflow. Read more about [Pipelines](../../register-and-refine/inventory-management/pipelines/index.md) to understand more about what they are and how they work. This guide covers how to register pipelines on the Corridor platform, using an **Intent Classification Pipeline** as a working example.

## Prerequisites

Before registering a pipeline, ensure you have:

- ✅ **Registered a Model** - Follow the [Model Registration Guide](../model/) to register Gemini 2.0 Flash

- ✅ **Registered a Prompt** - Follow the [Prompt Registration Guide](../prompt/) to register the intent classification prompt

**Quick Check:** Navigate to **GenAI Studio → Model Catalog** and **Prompt Registry** to verify your resources are available.

If you haven't completed these steps, please do so before proceeding.

---

## Registration Steps

### Step 1. Navigate to Pipeline Registry

Go to **GenAI Studio → Pipeline Registry** and click the **Create** button.

### Step 2. Fill in Basic Information

![alt text](image-3.png)

**Basic Information** fields help organize and identify your pipeline:

- **Description:** Clear explanation of what the pipeline does and its workflow
- **Usecase Type:** The primary use case category (e.g., "Question Answering")
- **Task Type:** Specific task the pipeline performs (e.g., "Classification")
- **Impact of Generated Output:** Scope of the pipeline's usage (e.g., "Internal Only")
- **Data Usage:** Whether the pipeline uses additional data sources beyond user input
- **Group:** Category for organizing similar pipelines (e.g., "Conversational AI ChatBot Pipeline")
- **Permissible Purpose:** Approved use cases and business scenarios for this pipeline

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

### Step 3. Configure Code Settings

![alt text](image-4.png)

**Code Settings** define how your pipeline operates and which resources it uses.

Fill in the **Basic Information** fields as shown in the image above. These includes Alias, Input Type, Pipeline Type, and Context Type.

NOTE: For this case we have chosen to create a chat-based pipeline as in future we can expand the pipeline to recognize the user's intent over multiple turns, though for now we are keeping it simple and using a single input/output.


### Step 4. Add Resources

**Resources** are the pre-registered components your pipeline will use.

Click **+ Create New** or search for existing resources to add:

**LLMs / Models:**

- `gemini_2_0_flash` - The foundation model for generating responses

**Prompts:**

- `customer_intent_classification_prompt` - The structured instructions for intent classification

**Other Resources** (Not required for this example):

- **RAGs:** For retrieving relevant documents
- **Agents & Sub-Pipelines:** For complex multi-step workflows
- **Helper Functions:** For data processing utilities, or any other function according to your requirement

### Step 5. Write Pipeline Scoring Logic

![alt text](image-5.png)

**Pipeline Scoring Logic** orchestrates how resources work together:

- Combines models, prompts, and other resources
- Processes user inputs and conversation history
- Generates outputs and maintains context across turns

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
    "output":  classified_intent,
    "context": "Any information that needs to be stored across turns"
}
```

**What This Does:**

1. Calls the Gemini model with the classification prompt and user message.
2. Parses the JSON response to extract the classified intent.
3. Validates the intent against the list of valid intents.
4. Returns the classification result as the output and any information that needs to be stored across turns as the context.

**Variables Available:**

- `user_message` - The current user input (type: String)
- `history` - Previous conversation messages (type: list[TypedDict[{'role': str, 'content': str}]])
- `context` - Any information that needs to be stored across turns (type: String)

### Step 6. Add Examples (Optional)

![alt text](image-6.png)

Add test examples to validate pipeline behavior.

**Note:** Examples help with testing and documenting expected behavior.

### Step 7. Save the Pipeline

Click **Create** to register the pipeline.

The pipeline is now:

- Available in the Pipeline Registry
- Ready for simulation and testing
- Ready for use in downstream applications

---

## Testing Your Pipeline

After creating the pipeline, test it to verify behavior:

### Quick Test (During Creation/Editing)

1. While creating or editing the pipeline, scroll to the **Code** section
2. Click **Test Code** in the bottom right corner
3. Enter test inputs to verify logic without saving

### Interactive Test (After Saving)

1. Navigate to your saved pipeline
2. Click **Run** → **Chat Session** (top right corner)
    
    NOTE: Chat sessions is only available for chat-based pipelines. For free-flow pipelines, you can test the pipeline by calling the pipeline function with sample inputs using the test code button.

3. Enter sample messages to test the full conversation flow
4. Verify outputs match expected behavior

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
classified_intent = result["output"]  # "BLOCK CARD"
context = result["context"]  # "Any information that needs to be stored across turns"
```

---

## Related Documentation

- [Model Registration Guide](../model/) - Register foundation models
- [Prompt Registration Guide](../prompt/) - Create reusable prompts

---

By following this guide, you can create reliable, production-ready pipelines that combine multiple AI resources into cohesive workflows.