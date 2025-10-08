# Setting up Integrations

Setup integrations to services that provide LLMs as an API. Configure your API keys once to access multiple AI providers across the platform.

## Getting Started

Navigate to **Settings > Platform Integrations** to configure your LLM providers. Each provider requires an API key that creates secure environment variables for your models.

## LLM Providers

### OpenAI
**Models available**: o4-mini, o3, o3-mini, etc

1. Click the OpenAI card
2. Enter your API key from platform.openai.com
3. Test connection and save

### Anthropic
**Models available**: claude-4-opus, claude-4-sonnet, claude-3.7-sonnet, etc

1. Click the Anthropic card
2. Enter your API key from console.anthropic.com
3. Test connection and save

### Azure AI
**Models available**: o4-mini, o3, o3-mini, etc

1. Click the Azure AI card
2. Enter your Azure OpenAI API key
3. Test connection and save

### Amazon Bedrock
**Models available**: amazon.titan-text-premier-v1:0, amazon.titan-text-express-v1, amazon.titan-text-lite-v1, etc

1. Click the Amazon Bedrock card
2. Configure AWS credentials:
   * **Access Key ID**: Your AWS access key
   * **Secret Access Key**: Your AWS secret key
   * **Session Token**: Optional temporary session token
   * **Default Region**: AWS region (e.g., us-east-1)
3. Test connection and save

### DeepSeek
**Models available**: deepseek-r1, deepseek-v3, deepseek-v2.5

1. Click the DeepSeek card
2. Get your API key from DeepSeek Platform
3. Enter your API key in the field
4. Click "Test Connection" to verify
5. Click "Save" to complete setup

### Google Vertex AI
**Models available**: gemini-2.5-pro, gemini-2.5-flash, gemini-2.0-flash, etc

1. Click the Google Vertex AI card
2. Upload service account JSON key
3. Test connection and save

### Hugging Face
**Models available**: llama-3.1-8b-instruct, llama-3.1-70b-instruct, llama-3.1-405b-instruct, etc

1. Click the Hugging Face card
2. Enter your HF token from huggingface.co/settings/tokens
3. Test connection and save

### Nvidia NIM 
**Models available**: llama-3.1-nemotron-instruct-70b, llama-3.3-nemotron-super-49b-reasoning, llama-3.1-nemotron-ultra-253b-v1-reasoning, etc

1. Click the Nvidia NIM card
2. Enter your Nvidia API key
3. Test connection and save

### GitHub Models
**Models available**: o4-mini, o3, o3-mini, etc

1. Click the GitHub Models card
2. Enter your GitHub token
3. Test connection and save

## Integration Status

* **Active**: Ready to use in model registration
* **Inactive**: Needs configuration or has connection issues

## Setting Up API Keys

Each integration creates environment variables that you can use in your model code:

* **OpenAI**: `OPENAI_API_KEY`
* **Anthropic**: `ANTHROPIC_API_KEY`
* **Azure AI**: `AZURE_ENDPOINT`
* **DeepSeek**: `DEEPSEEK_API_KEY`
* **Google Vertex AI**: `GOOGLE_API_TOKEN`
* **Hugging Face**: `HUGGING_FACE_HUB_TOKEN`
* **GitHub Models**: `GITHUB_TOKEN`
* **Amazon Bedrock**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_DEFAULT_REGION`

## Using Environment Variables

Once configured, the environment variables are automatically available in your model code:

```python
import os

# Access your API keys
openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
azure_endpoint = os.getenv("AZURE_ENDPOINT")
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
google_token = os.getenv("GOOGLE_API_TOKEN")
hf_token = os.getenv("HUGGING_FACE_HUB_TOKEN")
github_token = os.getenv("GITHUB_TOKEN")

# AWS Bedrock credentials
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.getenv("AWS_SESSION_TOKEN")
aws_region = os.getenv("AWS_DEFAULT_REGION")
```

## Need Help?

* Use "Test Connection" to verify your API keys
* Check provider documentation for API key setup
* Ensure proper permissions for your API keys