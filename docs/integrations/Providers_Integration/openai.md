# OpenAI Integration

The OpenAI integration provides direct access to OpenAI models through a unified interface. Configure once, use everywhere with enterprise-grade performance and the latest AI capabilities from OpenAI.

## Integrating OpenAI

Simply enter your OpenAI API key once in the Platform Integrations section. This enables authorized users to access OpenAI models within the platform. Once integrated, models can be registered and used as any other python object on the platform.

```python
# Example: Using a registered OpenAI model
result = openai_gpt4_model(text="Analyze this data", temperature=0.8)
```

## Example of Models Supported

OpenAI provides access to state-of-the-art language models with different capabilities:

**GPT-4o** - Most advanced multimodal model with vision and reasoning capabilities  
**GPT-4** - Advanced reasoning and complex task completion  
**GPT-3.5 Turbo** - Fast, efficient responses for most use cases  
**o1-preview, o1-mini** - Latest reasoning models with enhanced problem-solving  
**Additional Models** - Latest OpenAI variants with enhanced capabilities

## Registering a New OpenAI Model

Navigate to **New Model** to begin registration. The registration form connects your OpenAI integration with custom model configurations.

### Basic Information

**Description**: Document your model's purpose, use cases, and limitations. For example: "GPT-4o optimized for content analysis and generation. Use for enterprise content processing with multimodal capabilities. Ideal for complex reasoning and creative tasks."

### Code Configuration

**Alias**: A unique identifier for your model (e.g., `openai_gpt4_analyzer`, `content_generator`). This becomes the variable name you'll use in code.

**Output Type**: Define the return format:
- `Map[String, String]` - Key-value pairs for structured responses
- `String` - Simple text responses
- `List` - Array of items

**Input Type**: Select your implementation approach:
- **API Based**: Platform handles API calls automatically using your OpenAI integration
- **Python Function**: Custom function implementation with full control
- **Custom**: Advanced configurations for specialized use cases

**Model Provider**: Select "OpenAI" from your configured integrations.

### Arguments Configuration

Define input parameters that your model will accept. Important: Variables declared here are automatically available in the Scoring Logic section.

Common argument patterns for OpenAI models:

| Alias | Type | Optional | Default Value | Usage |
|-------|------|----------|---------------|-------|
| `text` | String | No | N/A | Main input content |
| `temperature` | Numerical | Yes | 0.7 | Controls response creativity |
| `max_tokens` | Numerical | Yes | 1500 | Maximum response length |
| `system_prompt` | String | Yes | "" | System instructions |

Use **+ Add Argument** to include additional parameters.

### Scoring Logic Implementation

In the Scoring Logic section, you can directly reference any variable declared in the Arguments section. The platform automatically makes these available in your code.

```python
# Arguments: text, temperature are automatically available
def init():
    import os
    from openai import OpenAI
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    return client

if "model" not in cache:
    cache["model"] = init()

client = cache["model"]

if text is None:
    return None

messages = [
    {"role": "system", "content": system_prompt if system_prompt else "You are a helpful assistant."},
    {"role": "user", "content": text}
]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    max_tokens=int(max_tokens),
    temperature=float(temperature),
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0
)

return {"response": completion.choices[0].message.content, "usage": completion.usage.total_tokens}
```

## Platform Integration Setup

Before registering models, configure your OpenAI credentials:

1. Navigate to **Settings > Platform Integrations**
2. Click on **OpenAI**
3. Enter your OpenAI API key
4. Test the connection

The platform creates environment variables automatically:
- `OPENAI_API_KEY`

## Example Use Case: Content Analysis Model

An OpenAI GPT-4o model configured for enterprise content analysis demonstrates the complete workflow:

### Arguments Configuration:
- `text` (String, required)
- `temperature` (Numerical, optional, default: "0.3")
- `max_tokens` (Numerical, optional, default: "2000")
- `system_prompt` (String, optional, default: "You are an expert content analyst.")

### Usage:
```python
# Model becomes available as: content_analyzer
result = content_analyzer(
    text="Your content text here...",
    temperature=0.3,
    max_tokens=2000,
    system_prompt="Analyze this content for key themes, sentiment, and actionable insights."
)
```

## Want to Learn More?

- Review [OpenAI API documentation](https://platform.openai.com/docs)
- Check [OpenAI model capabilities](https://platform.openai.com/docs/models)
- Monitor usage through OpenAI Dashboard
- Set up rate limiting and cost management