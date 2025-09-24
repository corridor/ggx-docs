# AWS Bedrock Integration

The AWS Bedrock integration provides access to foundation models from multiple AI providers through a unified interface. Configure once, use everywhere with enterprise-grade security, scalability, and comprehensive model selection from leading AI companies.

## Integrating AWS Bedrock

Configure your AWS credentials once in the Platform Integrations section. This enables authorized users to access Bedrock foundation models within the platform. Once integrated, models can be registered and used as any other python object on the platform.

```python
# Example: Using a registered Bedrock model
result = bedrock_claude_model(text="Analyze this data", temperature=0.8)
```

## Example of Models Supported

AWS Bedrock provides access to foundation models from multiple leading AI providers:

**Amazon Titan** - Amazon's own foundation models for text generation and embeddings  
**Anthropic Claude** - Claude 3.7 Sonnet, Claude 3.5 Sonnet, and other Claude variants  
**Meta Llama** - Llama 3.2 series with fine-tuning capabilities  
**Cohere Command** - Command R/R+ and Embed v3 families for text generation and embeddings  
**AI21 Labs Jamba** - Jamba 1.5 series for advanced language processing  
**Stability AI** - Stable Diffusion series for image generation  
**Additional Models** - +122 models available through Amazon Bedrock Marketplace

## Registering a New Bedrock Model

Navigate to **New Model** to begin registration. The registration form connects your AWS Bedrock integration with custom model configurations.

### Basic Information

**Description**: Document your model's purpose, use cases, and limitations. For example: "Claude 3.7 Sonnet on AWS Bedrock optimized for enterprise content analysis. Use for document processing with AWS compliance features. Ideal for complex reasoning and multi-step analysis tasks."

### Code Configuration

**Alias**: A unique identifier for your model (e.g., `bedrock_claude_analyzer`, `titan_embedder`). This becomes the variable name you'll use in code.

**Output Type**: Define the return format:
- `Map[String, String]` - Key-value pairs for structured responses
- `String` - Simple text responses
- `List` - Array of items

**Input Type**: Select your implementation approach:
- **API Based**: Platform handles API calls automatically using your AWS integration
- **Python Function**: Custom function implementation with full control
- **Custom**: Advanced configurations for specialized use cases

**Model Provider**: Select "Amazon Bedrock" from your configured integrations.

### Arguments Configuration

Define input parameters that your model will accept. Important: Variables declared here are automatically available in the Scoring Logic section.

Common argument patterns for Bedrock models:

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
    import boto3
    
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        aws_session_token=os.getenv("AWS_SESSION_TOKEN")
    )
    return client

if "model" not in cache:
    cache["model"] = init()

client = cache["model"]

if text is None:
    return None

# Prepare the conversation for Claude models
conversation = [
    {
        "role": "user",
        "content": [{"text": text}]
    }
]

# Add system message if provided
if system_prompt:
    conversation.insert(0, {
        "role": "system", 
        "content": [{"text": system_prompt}]
    })

try:
    response = client.converse(
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",
        messages=conversation,
        inferenceConfig={
            "temperature": float(temperature),
            "maxTokens": int(max_tokens)
        }
    )
    
    return {
        "response": response["output"]["message"]["content"][0]["text"],
        "usage": response["usage"]["inputTokens"] + response["usage"]["outputTokens"]
    }
except Exception as e:
    return {"error": str(e)}
```

## Platform Integration Setup

Before registering models, configure your AWS credentials:

1. Navigate to **Settings > Platform Integrations**
2. Click on **Amazon Bedrock**
3. Configure AWS credentials:
   * **Access Key ID**: Your AWS access key
   * **Secret Access Key**: Your AWS secret key
   * **Session Token**: Optional temporary session token
   * **Default Region**: AWS region (e.g., us-east-1)
4. Test the connection

The platform creates environment variables automatically:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- `AWS_DEFAULT_REGION`

## Example Use Case: Document Analysis Model

An AWS Bedrock Claude model configured for enterprise document analysis demonstrates the complete workflow:

### Arguments Configuration:
- `text` (String, required)
- `temperature` (Numerical, optional, default: "0.3")
- `max_tokens` (Numerical, optional, default: "2000")
- `system_prompt` (String, optional, default: "You are an expert document analyst.")

### Usage:
```python
# Model becomes available as: document_analyzer
result = document_analyzer(
    text="Your document content here...",
    temperature=0.3,
    max_tokens=2000,
    system_prompt="Analyze this document for key insights, themes, and actionable recommendations."
)
```

## Want to Learn More?

- Review [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
- Check [supported foundation models](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html)
- Monitor usage through AWS Console
- Set up cost management and billing alerts