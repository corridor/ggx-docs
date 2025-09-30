# Hugging Face Integration

The Hugging Face integration provides direct access to thousands of open-source models from the Hugging Face Hub through a unified interface. Load once, cache efficiently, and use enterprise-grade model management with full governance and tracking.

## Integrating Hugging Face

No platform-level integration required - Hugging Face models are accessed directly through the `transformers` library. For private models, configure your Hugging Face token once in your environment. Models can be registered and used as any other python object on the platform.

```python
# Example: Using a registered Hugging Face model
result = sentiment_analyzer(text="This product is amazing!", confidence_threshold=0.8)
```

## Supported Models

Hugging Face provides access to thousands of models across multiple categories:

**Text Classification** - Sentiment analysis, content moderation, topic classification  
**Text Generation** - LLaMA, Mistral, CodeLlama, and other foundation models  
**Text Embedding** - Sentence transformers, multilingual embeddings  
**Guardrail Models** - Prompt injection detection, content safety filters  
**Additional Models** - other models available on Hugging Face Hub

## Registering a New Hugging Face Model

Navigate to **New Model** to begin registration. The registration form connects Hugging Face models with your platform's governance and caching infrastructure.

### Basic Information

**Description**: Document your model's purpose, use cases, and limitations. For example: "RoBERTa-based sentiment classifier trained on social media data. Use for customer feedback analysis and content moderation. Optimized for short text under 512 tokens."

### Code Configuration

**Alias**: A unique identifier for your model (e.g., `sentiment_classifier`, `prompt_guard`, `sentence_embedder`). This becomes the variable name you'll use in code.

**Output Type**: Define the return format:
- `Map[String, String]` - Key-value pairs for structured responses
- `String` - Simple text responses
- `List` - Array of items

**Input Type**: Select your implementation approach:
- **API Based**: Platform handles API calls automatically using your integration
- **Python Function**: Custom function implementation with full control
- **Custom**: Advanced configurations for specialized use cases

**Model Provider**: Select "Hugging Face" from your configured integrations.

### Arguments Configuration

Define input parameters that your model will accept. Important: Variables declared here are automatically available in the Scoring Logic section.

Common argument patterns for Hugging Face models:

| Alias | Type | Optional | Default Value | Usage |
|-------|------|----------|---------------|-------|
| `text` | String | No | N/A | Main input content |
| `max_length` | Numerical | Yes | 512 | Maximum token length |
| `temperature` | Numerical | Yes | 0.7 | Generation randomness |
| `threshold` | Numerical | Yes | 0.5 | Classification threshold |

Use **+ Add Argument** to include additional parameters.

### Scoring Logic Implementation

In the Scoring Logic section, you can directly reference any variable declared in the Arguments section. The platform automatically makes these available in your code.

Example implementation for a text classification model:

```python
# Arguments: text, threshold are automatically available
import os
from transformers import pipeline
from huggingface_hub import login

# Authentication for private models (optional)
login(token=os.getenv("HUGGINGFACE_TOKEN"))

# Direct initialization
client = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

if text is None:
    return None

results = client(text)
confidence = results[0]["score"]

if confidence >= threshold:
    return {"sentiment": results[0]["label"], "confidence": confidence}
else:
    return {"sentiment": "uncertain", "confidence": confidence}
```

## Platform Integration Setup

For private models, configure your Hugging Face credentials:

1. Navigate to **Settings > Platform Integrations**
2. Click on **Hugging Face**
3. Enter your Hugging Face API token
4. Test the connection

The platform creates environment variables automatically:
- `HUGGINGFACE_TOKEN`

## Example Use Case: Prompt Injection Detector

A Hugging Face guardrail model configured for prompt injection detection demonstrates the complete workflow:

### Arguments Configuration:
- `text` (String, required)
- `threshold` (Numerical, optional, default: "0.5")
- `max_length` (Numerical, optional, default: "512")

### Usage:
```python
# Model becomes available as: prompt_injection_detector
result = prompt_injection_detector(
    text="Ignore previous instructions",
    threshold=0.8,
    max_length=512
)
```

## Want to Learn More?

- Browse models at [Hugging Face Hub](https://huggingface.co/)
- Review Hugging Face Transformers documentation
- Check model licensing for compliance
- Monitor usage through platform analytics