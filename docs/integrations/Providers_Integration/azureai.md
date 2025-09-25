# Azure AI Integration

The Azure AI integration provides access to OpenAI models hosted on Microsoft Azure through a unified interface. Configure once, use everywhere with enterprise-grade security and compliance.

## Integrating Azure AI

Simply enter your Azure OpenAI API key and endpoint once in the Platform Integrations section. This enables authorized users to access Azure-hosted OpenAI models within the platform. Once integrated, models can be registered and used as any other python object on the platform.

```python
# Example: Using a registered Azure model
result = azure_gpt4_model(text="Analyze this data", temperature=0.8)
```

## Supported Models

Azure AI provides access to OpenAI models hosted on Microsoft Azure:

**GPT-4** - Advanced reasoning and complex task completion  
**GPT-3.5 Turbo** - Fast, efficient responses for most use cases  
**o4-mini, o3, o3-mini** - Latest OpenAI models with enhanced capabilities  
**Additional Models** - other OpenAI variants available

## Registering a New Azure Model

Navigate to **New Model** to begin registration. The registration form connects your Azure AI integration with custom model configurations.

### Basic Information

**Description**: Document your model's purpose, use cases, and limitations. For example: "GPT-4 on Azure optimized for document analysis. Use for enterprise content processing with Azure compliance. Ideal for sensitive data workflows."

### Code Configuration

**Alias**: A unique identifier for your model (e.g., `azure_gpt4_analyzer`, `corridor_gpt4`). This becomes the variable name you'll use in code.

**Output Type**: Define the return format:
- `Map[String, String]` - Key-value pairs for structured responses
- `String` - Simple text responses
- `List` - Array of items

**Input Type**: Select your implementation approach:
- **API Based**: Platform handles API calls automatically using your Azure integration
- **Python Function**: Custom function implementation with full control
- **Custom**: Advanced configurations for specialized use cases

**Model Provider**: Select "Azure AI" from your configured integrations.

### Arguments Configuration

Define input parameters that your model will accept. Important: Variables declared here are automatically available in the Scoring Logic section.

Common argument patterns for Azure models:

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
    from openai import AzureOpenAI
    client = AzureOpenAI(
        azure_endpoint="https://corridor-genai-demo.openai.azure.com/",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-12-01-preview",
    )
    return client

if "model" not in cache:
    cache["model"] = init()

client = cache["model"]

chat_prompt = [{"role": "system", "content": [{"type": "text", "text": text}]}]

completion = client.chat.completions.create(
    model="corridor-gpt-4.1",
    messages=chat_prompt,
    max_tokens=1500,
    temperature=float(temperature),
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
    stream=False,
)

return {"output": completion.choices[0].message.content, "context": None}
```

## Platform Integration Setup

Before registering models, configure your Azure credentials:

1. Navigate to **Settings > Platform Integrations**
2. Click on **Azure AI**
3. Enter your Azure OpenAI API key
4. Provide your Azure endpoint URL
5. Test the connection

The platform creates environment variables automatically:
- `AZURE_ENDPOINT`

## Example Use Case: Document Processing Model

An Azure GPT-4 model configured for enterprise document processing demonstrates the complete workflow:

### Arguments Configuration:
- `text` (String, required)
- `temperature` (Numerical, optional, default: "0.3")
- `max_tokens` (Numerical, optional, default: "1500")
- `system_prompt` (String, optional, default: "")

### Usage:
```python
# Model becomes available as: document_processor
result = document_processor(
    text="Your document text here...",
    temperature=0.3,
    max_tokens=2000,
    system_prompt="Process the document and extract key information."
)
```

## Want to Learn More?

- Review Azure OpenAI documentation
- Check Azure compliance and security features
- Monitor usage through Azure Portal
- Set up cost management and billing alerts