# Anthropic Integration

The Anthropic integration provides access to Claude models through a unified interface. Configure once, use everywhere with enterprise-grade safety features and constitutional AI principles built into every interaction.

## Integrating Anthropic

Simply enter your Anthropic API key once in the Platform Integrations section. This enables authorized users to access Claude models within the platform. Once integrated, models can be registered and used as any other python object on the platform.

```python
# Example: Using a registered Anthropic model
result = claude_sonnet_model(text="Analyze this document", max_tokens=1500)
```

## Example of Models Supported

Anthropic provides access to Claude models with different capabilities and performance characteristics:

**Claude 3.5 Sonnet** - Balanced performance for most use cases with strong reasoning  
**Claude 3 Opus** - Most capable model for complex tasks requiring deep analysis  
**Claude 3 Haiku** - Fast, cost-effective model for simple tasks  
**Claude 3.5 Haiku** - Enhanced version with improved speed and capabilities  
**Additional Models** - Latest Claude variants with enhanced reasoning capabilities

## Registering a New Anthropic Model

Navigate to **New Model** to begin registration. The registration form connects your Anthropic integration with custom model configurations.

### Basic Information

**Description**: Document your model's purpose, use cases, and limitations. For example: "Claude 3.5 Sonnet optimized for document analysis and content generation. Use for enterprise content processing with built-in safety features. Ideal for complex reasoning tasks and multi-step analysis."

### Code Configuration

**Alias**: A unique identifier for your model (e.g., `claude_sonnet_analyzer`, `claude_document_processor`). This becomes the variable name you'll use in code.

**Output Type**: Define the return format:
- `Map[String, String]` - Key-value pairs for structured responses
- `String` - Simple text responses
- `List` - Array of items

**Input Type**: Select your implementation approach:
- **API Based**: Platform handles API calls automatically using your Anthropic integration
- **Python Function**: Custom function implementation with full control
- **Custom**: Advanced configurations for specialized use cases

**Model Provider**: Select "Anthropic" from your configured integrations.

### Arguments Configuration

Define input parameters that your model will accept. Important: Variables declared here are automatically available in the Scoring Logic section.

Common argument patterns for Anthropic models:

| Alias | Type | Optional | Default Value | Usage |
|-------|------|----------|---------------|-------|
| `text` | String | No | N/A | Main input content |
| `max_tokens` | Numerical | Yes | 1500 | Maximum response length |
| `temperature` | Numerical | Yes | 0.7 | Controls response creativity |
| `system_prompt` | String | Yes | "" | System instructions |

Use **+ Add Argument** to include additional parameters.

### Scoring Logic Implementation

In the Scoring Logic section, you can directly reference any variable declared in the Arguments section. The platform automatically makes these available in your code.

Example implementation for a text analysis model:

```python
# Arguments: text, max_tokens, temperature are automatically available
import os
import anthropic

# Direct initialization
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

if text is None:
    return None

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=int(max_tokens),
    temperature=float(temperature),
    system=system_prompt if system_prompt else "You are a helpful AI assistant.",
    messages=[
        {"role": "user", "content": text}
    ]
)

return {"output": message.content[0].text, "context": None}
```

## Platform Integration Setup

Before registering models, configure your Anthropic credentials:

1. Navigate to **Settings > Platform Integrations**
2. Click on **Anthropic**
3. Enter your Anthropic API key
4. Test the connection

The platform creates environment variables automatically:
- `ANTHROPIC_API_KEY`

## Example Use Case: Document Analysis Model

An Anthropic Claude model configured for enterprise document analysis demonstrates the complete workflow:

### Arguments Configuration:
- `text` (String, required)
- `max_tokens` (Numerical, optional, default: "2000")
- `temperature` (Numerical, optional, default: "0.3")
- `system_prompt` (String, optional, default: "You are a helpful document analysis assistant.")

### Usage:
```python
# Model becomes available as: claude_document_analyzer
result = claude_document_analyzer(
    text="Your document text here...",
    max_tokens=2000,
    temperature=0.3,
    system_prompt="Analyze this document and provide key insights with detailed explanations."
)
```

## Want to Learn More?

- Review [Anthropic documentation](https://docs.anthropic.com/)
- Check [Claude model capabilities](https://www.anthropic.com/claude)
- Monitor usage through Anthropic Console
- Set up rate limiting and cost management