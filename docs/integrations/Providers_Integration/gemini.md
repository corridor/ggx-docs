# Google Cloud Vertex AI Integration

The Google Cloud Vertex AI integration provides access to Gemini models and AI agents through a unified interface. Configure once, use everywhere with enterprise-grade security and scalability.

## Integrating Google Cloud Vertex AI

Simply upload your service account JSON key once in the Platform Integrations section. This enables authorized users to access Google Cloud Vertex AI models within the platform. Once integrated, models can be registered and used as any other python object on the platform.

```python
# Example: Using a registered Gemini model
result = gemini_model(text="Analyze this data", temperature=0.8)
```

## Supported Models

Google Cloud Vertex AI provides access to Gemini models and agents:

**Gemini 2.5 Pro** - Advanced reasoning and multimodal capabilities  
**Gemini 2.5 Flash** - Fast, efficient responses for high-volume use cases  
**Gemini 2.0 Flash** - Latest generation model with improved performance  
**Additional Models** - other Gemini variants available

## Registering a New Gemini Model

Navigate to **New Model** to begin registration. The registration form connects your Google Cloud integration with custom model configurations.

### Basic Information

**Description**: Document your model's purpose, use cases, and limitations. For example: "Gemini 2.5 Pro optimized for content analysis. Use for document summarization and multimodal tasks. Ideal for complex reasoning workflows."

### Code Configuration

**Alias**: A unique identifier for your model (e.g., `gemini_analyzer`, `content_summarizer`). This becomes the variable name you'll use in code.

**Output Type**: Define the return format:
- `Map[String, String]` - Key-value pairs for structured responses
- `String` - Simple text responses
- `List` - Array of items

**Input Type**: Select your implementation approach:
- **API Based**: Platform handles API calls automatically using your Google Cloud integration
- **Python Function**: Custom function implementation with full control
- **Custom**: Advanced configurations for specialized use cases

**Model Provider**: Select "Google Vertex AI" from your configured integrations.

### Arguments Configuration

Define input parameters that your model will accept. Important: Variables declared here are automatically available in the Scoring Logic section.

Common argument patterns for Gemini models:

| Alias | Type | Optional | Default Value | Usage |
|-------|------|----------|---------------|-------|
| `text` | String | No | N/A | Main input content |
| `temperature` | Numerical | Yes | 0.7 | Controls response creativity |
| `system_instruction` | String | Yes | "" | System prompt for model behavior |
| `seed` | Numerical | Yes | 2025 | Deterministic generation seed |

Use **+ Add Argument** to include additional parameters.

### Scoring Logic Implementation

In the Scoring Logic section, you can directly reference any variable declared in the Arguments section. The platform automatically makes these available in your code.

```python
# Arguments: text, temperature, system_instruction are automatically available
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GOOGLE_API_TOKEN"))

config = types.GenerateContentConfig(
    temperature=temperature, 
    seed=2025, 
    system_instruction=system_instruction
)

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=text, 
    config=config
)

return {"response": response.text}
```

## Platform Integration Setup

Before registering models, configure your Google Cloud credentials:

1. Navigate to **Settings > Platform Integrations**
2. Click on **Google Vertex AI**
3. Upload your service account JSON key file
4. Enter your Google Cloud project ID
5. Test the connection

The platform creates environment variables automatically:
- `GOOGLE_API_TOKEN`
- `GOOGLE_CLOUD_PROJECT`

## Example Use Case: Content Analysis Model

A Gemini 2.5 Pro model configured for content analysis demonstrates the complete workflow:

### Arguments Configuration:
- `text` (String, required)
- `temperature` (Numerical, optional, default: "0.3")
- `system_instruction` (String, optional, default: "You are an expert content analyst.")
- `seed` (Numerical, optional, default: "2025")

### Usage:
```python
# Model becomes available as: content_analyzer
result = content_analyzer(
    text="Your document content here...",
    temperature=0.3,
    system_instruction="Provide a comprehensive analysis with key insights and recommendations.",
    seed=2025
)
```

## Want to Learn More?

- Review Google Cloud Vertex AI documentation
- Check Gemini model specifications
- Monitor usage and costs through Google Cloud Console
- Set up billing alerts for cost management