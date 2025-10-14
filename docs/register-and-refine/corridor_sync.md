## Overview

The GenGuardX Corridor Sync system enables you to programmatically manage and version-control your AI assets (Prompts, Models, RAGs, Pipelines, Global Functions, and Reports) directly from your development environment. Using Python decorators and a simple sync command, you can declare and synchronize your components to the GenGuardX platform.

---

## What Can Be Synced?

GenGuardX Corridor Sync supports six core component types:

| Component | Purpose | Example Use Case |
| --- | --- | --- |
| **Prompt** | System instructions, templates, and persona definitions | Customer service chatbot instructions |
| **Model** | LLM configurations and API integrations | Gemini, GPT, Claude model wrappers |
| **RAG** | Retrieval-Augmented Generation systems | Database query systems, knowledge base retrieval |
| **Pipeline** | End-to-end workflows combining multiple components | Complete chatbot with intent classification and response generation |
| **Global Function** | Reusable utility functions | Data preprocessing, validation, formatting functions |
| **Report** | Evaluation and monitoring reports with visualizations | Model performance dashboards, bias analysis reports |

---

## Getting Started

### Step 1: Installation

```bash
pip install genguardx

```

### Step 2: Initialize Connection

Before syncing any components, you need to authenticate with your GenGuardX instance.

### Obtaining Your API Key

1. Log into your GenGuardX platform
2. Navigate to **Profile Section** → **Account Security**
3. Locate your **API Key** (format: `eyJI-XXXX-XXXX-XXXX-XXXX-XXXX-3fe3`)
4. Click **"How to use this key"** to view the initialization code

### Initialize in Your Code

```python
import genguardx as ggx

# Initialize connection to your GenGuardX instance
ggx.init(
    api_url="https://devaisandbox.corridorplatforms.com",  # Change for your instance
    api_key="your-api-key-here",
)

```

> Important: Replace the api_url if you're using a different GenGuardX instance (e.g., production, staging). The URL should point to your specific deployment.
> 

---

## Component Declaration & Sync

Each component type uses a specific decorator pattern. Components can be declared and synced **independently** or used together in pipelines.

### 1. Prompts

Prompts define system instructions, templates, or conversation guidelines.

### Decorator Syntax

```python
import genguardx as ggx
@ggx.Prompt.declare(
    name='My Prompt Name',           # Optional: defaults to function name
    group='My Group',                # Optional: organizational grouping
    task_type='Question Answering',  # Optional: Classification | Summarization | etc.
    prompt_type='System Instruction', # Optional: User Prompt | Others
    prompt_elements=['Persona + Goal', 'Tone', 'Constraints'],  # Optional: list of components
)
def my_prompt_function(*, cache: dict = {}, prompt: str = "Your prompt text here"):
    """Docstring describing the prompt purpose."""
    # -- BEGIN DEFINITION --
    return prompt

# Sync to platform
ggx.sync(my_prompt_function)

```

---

### 2. Models

Models wrap LLM API calls with consistent interfaces and cost tracking.

### Decorator Syntax

```python
import genguardx as ggx
@ggx.Model.declare(
    name='My Model Name',          # Optional: defaults to function name
    group='My Group',              # Optional: organizational grouping
    ownership_type='Proprietary',  # Optional: Proprietary | Open Source
    model_type='LLM',              # Optional: LLM | Text Embedding | Guardrail | Judge Model | Others
    provider='openai',             # Optional: openai | google | anthropic | etc. (for API-based models)
    model='gpt-4',                 # Optional: specific model identifier (required if provider is set)
)
def my_model_function(text: str, temperature: float = 0.7, *, cache: dict = {}):
    """Docstring describing the model configuration."""
    # -- BEGIN DEFINITION --
    # Your model implementation
    return {"response": "...", "cost": "..."}

# Sync to platform
ggx.sync(my_model_function)

```

---

### 3. RAGs (Retrieval-Augmented Generation)

RAGs connect to knowledge bases, databases, or document stores to retrieve relevant context.

### Decorator Syntax

```python
import pathlib
import genguardx as ggx
@ggx.Rag.declare(
    name='My RAG System',                    # Optional: defaults to function name
    group='My Group',                        # Optional: organizational grouping
    knowledge_base_format='Relational Database',    # Optional: Vector Database | Graph Database | etc.
    provider=None,                           # Optional: provider identifier for API-based RAG systems
)
def my_rag_function(
    query: str,
    *,
    cache: dict = {},
    knowledge: pathlib.Path = pathlib.Path('data.db')
):
    """Docstring describing the RAG system."""
    # -- BEGIN DEFINITION --
    # Your RAG implementation
    return {"retrieved_data": "...", "query_used": "..."}

# Sync to platform
ggx.sync(my_rag_function)

```

---

### 4. Pipelines

Pipelines orchestrate multiple components into complete workflows.

### Decorator Syntax

```python
import typing as t
import genguardx as ggx
@ggx.Pipeline.declare(
    name='My Pipeline',                    # Optional: defaults to function name
    group='My Group',                      # Optional: organizational grouping
    usecase_type='Question Answering',     # Optional: Summarization | Translation
    task_type='Generative Responses',      # Optional: Classification | Templated Responses | etc.
    impact='External Facing',              # Optional: Internal Only | Internal - with external implications
    data_usage=['Customer Specific Data'], # Optional: list of data types
    pipeline_type='Chat based - OpenAI Spec',  # Required: or 'Custom Return Type'
)
def my_pipeline_function(
    user_message: str,
    history: list[t.TypedDict("T", {'role': str, 'content': str}, total=False)] = (),
    context: t.Optional[dict[str, str]] = None,
    *,
    cache: dict = {},
):
    """Docstring describing the pipeline workflow."""
    # -- BEGIN DEFINITION --
    # Your pipeline implementation
    return {"output": "...", "context": "..."}

# Sync to platform
ggx.sync(my_pipeline_function)

```

---

### 5. Global Functions

Global Functions are reusable utility functions that can be referenced by other components.

### Decorator Syntax

```python
import genguardx as ggx
@ggx.GlobalFunction.declare(
    name='My Utility Function',  # Optional: defaults to function name
    group='My Group',            # Optional: organizational grouping
)
def my_utility_function(input_text: str, max_length: int = 100, *, cache: dict = {}) -> str:
    """Docstring describing the utility function."""
    # -- BEGIN DEFINITION --
    # Your utility function implementation
    return input_text[:max_length]

# Sync to platform
ggx.sync(my_utility_function)

```

**Key Points**:

- Global Functions can be called by other components (Pipelines, RAGs, Models, etc.)

---

### 6. Reports

Reports generate evaluation dashboards with metrics and visualizations for monitoring AI systems.

### Decorator Syntax

```python
import typing as t
import genguardx as ggx
@ggx.Report.declare(
    name='My Evaluation Report',                     # Optional: defaults to function name
    object_types=['PIPELINE', 'FOUNDATION_MODEL'],   # Required: list of object types this report evaluates
    group='My Group',                                # Optional: organizational grouping
    risk_type='Accuracy',                            # Optional: Accuracy | Stability | Bias | Vulnerability | Toxicity | Others
    task_type='Classification',                      # Optional: Classification | Templated Responses | etc.
    risk_domain='Model Risk Management',             # Optional: Model Risk Management | Fair Lending | Technology | Infosec | Others
    evaluation_methodology='Statistical / ML Algorithms',  # Optional: LLM-as-a-Judge | Rule-based | Statistical / ML Algorithms | Others
    report_methodology='Custom methodology',          # Optional: free text description
    parameters=[],                                   # Optional: list of report parameters
)
def my_evaluation_report(job: t.Any, data: t.Any, *, cache: dict = {}) -> t.Any:
    """Docstring describing the report purpose."""
    # -- BEGIN DEFINITION --
    # Your report logic here
    # Process data and return metrics
    return metrics_dict, processed_data

# Sync to platform
ggx.sync(my_evaluation_report)

```

**Key Points**:

- Reports typically work with **ReportOutput**, **DataLogicExample**, and **AdditionalReportFigure** helper components
- Helper components use the `report` parameter to associate with their parent report (e.g., `report='My Evaluation Report'`)
- Report functions typically receive `job` and `data` parameters and return processed results
- ReportOutput functions generate visualizations (Plotly figures, Pandas DataFrames, or HTML/Markdown strings)

## Key Concepts

### The `# -- BEGIN DEFINITION --` Anchor

Every component function **must** include this special comment. Only code after this anchor is synced to the platform.

```python
def my_function():
    # Imports and setup code here (NOT synced)
    import os

    # -- BEGIN DEFINITION --
    # Everything after this line IS synced
    result = process_data()
    return result

```

**Why?** This ensures only the core logic is synced, keeping your platform definitions clean and portable.

### The `cache` Parameter

All component functions include a `cache: dict = {}` parameter. This is a **reserved keyword** that is:

- Automatically removed from function inputs during sync (not exposed to end users)
- Commonly used for storing database connections in RAG implementations

**Example from RAG:**

```python
if "sql_cursor_obj" not in cache:
    conn = sqlite3.connect(...)
    cache["sql_cursor_obj"] = conn.cursor()
cursor = cache["sql_cursor_obj"]

```

### Dependency Resolution

When you sync a Pipeline, the system:

1. Inspects the function bytecode to find referenced objects
2. Checks if those objects have `_corridor_metadata`
3. Recursively syncs those dependencies by calling their respective sync handlers
4. Collects the version IDs returned from each sync operation
5. Includes those version IDs in the pipeline payload (e.g., `promptVersionIds`, `foundationModelVersionIds`)

**Example:**

```python
# Define components
import genguardx as ggx
@ggx.Prompt.declare(name='System Prompt')
def system_prompt(*, cache: dict = {}, prompt: str = "You are a helpful assistant."):
    """System instruction for the assistant."""
    # -- BEGIN DEFINITION --
    return prompt

@ggx.Model.declare(name='GPT-4', provider='openai', model='gpt-4', ownership_type='Proprietary', model_type='LLM')
def gpt4(text: str, *, cache: dict = {}):
    """GPT-4 model wrapper."""
    # -- BEGIN DEFINITION --
    # Implementation
    return {"response": "..."}

@ggx.Pipeline.declare(name='Q&A Pipeline', pipeline_type='Chat based - OpenAI Spec')
def qa_pipeline(
    user_message: str,
    history: list[t.TypedDict("T", {'role': str, 'content': str}, total=False)] = (),
    context: t.Optional[dict[str, str]] = None,
    *,
    cache: dict = {}
):
    """Q&A pipeline combining prompt and model."""
    # -- BEGIN DEFINITION --
    prompt = system_prompt()
    response = gpt4(f"{prompt}\n{user_message}")
    return {"output": response["response"]}

# Sync only the pipeline - dependencies sync automatically
ggx.sync(qa_pipeline)

```

---

## Independent vs. Pipeline Usage

### Independent Sync

You can declare and sync components **without** using them in a pipeline:

```python
# Declare a standalone prompt
@ggx.Prompt.declare(name='Greeting Prompt', group='Standalone')
def greeting_prompt(*, cache: dict = {}, prompt: str = "Hello! How can I help you today?"):
    """Greeting message prompt."""
    # -- BEGIN DEFINITION --
    return prompt

# Sync it independently
ggx.sync(greeting_prompt)

```

### Pipeline Integration

Or use components together in a pipeline (they'll sync automatically):

```python
@ggx.Pipeline.declare(name='Greeter Bot', pipeline_type='Chat based - OpenAI Spec')
def greeter_pipeline(
    user_message: str,
    history: list[t.TypedDict("T", {'role': str, 'content': str}, total=False)] = (),
    context: t.Optional[dict[str, str]] = None,
    *,
    cache: dict = {}
):
    """Simple greeter pipeline."""
    # -- BEGIN DEFINITION --
    prompt = greeting_prompt()  # References the prompt
    return {"output": prompt}

ggx.sync(greeter_pipeline)  # Syncs both prompt and pipeline

```

---

## Metadata Parameters Reference

### Common Parameters (All Components)

- `name` (str, optional): Display name on platform. Defaults to function name.
- `group` (str, optional): Organizational grouping. Must exist on platform.

### Prompt-Specific Parameters

- `task_type` (str, optional): `'Classification'` | `'Question Answering'` | `'Information Extraction'` | `'Summarization'` | `'Code Generation'` | `'Transformation'` | `'Generation'` | `'Others'`
- `prompt_type` (str, optional): `'System Instruction'` | `'User Prompt'` | `'Others'`
- `prompt_elements` (list, optional): List of components: `['Persona + Goal', 'Tone', 'Task', 'Constraints', 'Context', 'Examples', 'Reasoning Steps', 'Output Format', 'Recap']`

### Model-Specific Parameters

- `ownership_type` (str, optional): `'Open Source'` | `'Proprietary'`
- `model_type` (str, optional): `'LLM'` | `'Text Embedding'` | `'Guardrail'` | `'Judge Model'` | `'Others'`
- `provider` (str, optional): Provider identifier (e.g., `'openai'`, `'google'`, `'anthropic'`). If provided, model is treated as API-based.
- `model` (str, optional): Specific model identifier (e.g., `'gpt-4'`, `'gemini-pro'`, `'claude-3-opus'`). Required if provider is specified.

### RAG-Specific Parameters

- `knowledge_base_format` (str, optional): `'Vector Database'` | `'Graph Database'` | `'Relational Database'` | `'External Web-Search APIs'` | `'NoSQL'` | `'Document'` | `'Others'`
- `provider` (str, optional): Provider identifier for API-based RAG systems.

### Pipeline-Specific Parameters

- `usecase_type` (str, optional): `'Question Answering'` | `'Summarization'` | `'Translation'`
- `task_type` (str, optional): `'Classification'` | `'Templated Responses'` | `'Generative Responses'` | `'Summarization'` | `'Others'`
- `impact` (str, optional): `'External Facing'` | `'Internal Only'` | `'Internal - with external implications'`
- `data_usage` (list, optional): List of data types: `['No Additional Data', 'General Public Data', 'Internal Policies/Data', 'Customer Specific Data']`
- `pipeline_type` (str, required): `'Chat based - OpenAI Spec'` | `'Custom Return Type'`

### Global Function Parameters

- `name` (str, optional): Display name on platform. Defaults to function name.
- `group` (str, optional): Organizational grouping. Must exist on platform.

### Report-Specific Parameters

- `object_types` (list, required): List of object types the report evaluates (e.g., `['PIPELINE', 'FOUNDATION_MODEL', 'PROMPT']`)
- `name` (str, optional): Display name on platform. Defaults to function name.
- `group` (str, optional): Organizational grouping. Must exist on platform.
- `risk_type` (str, optional): `'Accuracy'` | `'Stability'` | `'Bias'` | `'Vulnerability'` | `'Toxicity'` | `'Others'`
- `task_type` (str, optional): `'Classification'` | `'Templated Responses'` | `'Generative Responses'` | `'Summarization'` | `'Others'`
- `risk_domain` (str, optional): `'Model Risk Management'` | `'Fair Lending'` | `'Technology'` | `'Infosec'` | `'Others'`
- `evaluation_methodology` (str, optional): `'LLM-as-a-Judge'` | `'Rule-based'` | `'Statistical / ML Algorithms'` | `'Others'`
- `report_methodology` (str, optional): Free-text description of the methodology
- `parameters` (list, optional): List of parameter dictionaries for report execution

---

## Complete Workflow Example

```python
import genguardx as ggx
import typing as t

# Step 1: Initialize
ggx.init(
    api_url="https://devaisandbox.corridorplatforms.com",
    api_key="your-api-key-here",
)

# Step 2: Declare components
@ggx.Prompt.declare(
    name='FAQ Prompt',
    group='Support',
    task_type='Question Answering',
    prompt_type='System Instruction',
)
def faq_prompt(*, cache: dict = {}, prompt: str = "Answer FAQs concisely and professionally."):
    """System prompt for FAQ bot."""
    # -- BEGIN DEFINITION --
    return prompt

@ggx.Model.declare(
    name='GPT-3.5',
    group='Models',
    ownership_type='Proprietary',
    model_type='LLM',
    provider='openai',
    model='gpt-3.5-turbo',
)
def gpt35(text: str, *, cache: dict = {}):
    """GPT-3.5 Turbo model wrapper."""
    # -- BEGIN DEFINITION --
    # Implementation here
    return {"response": "..."}

@ggx.Pipeline.declare(
    name='FAQ Bot',
    group='Support',
    usecase_type='Question Answering',
    task_type='Templated Responses',
    impact='External Facing',
    data_usage=['General Public Data'],
    pipeline_type='Chat based - OpenAI Spec',
)
def faq_pipeline(
    user_message: str,
    history: list[t.TypedDict("T", {'role': str, 'content': str}, total=False)] = (),
    context: t.Optional[dict[str, str]] = None,
    *,
    cache: dict = {}
):
    """Complete FAQ pipeline."""
    # -- BEGIN DEFINITION --
    prompt = faq_prompt()
    response = gpt35(f"{prompt}\n\nQuestion: {user_message}")
    return {"output": response["response"]}

# Step 3: Sync (syncs all dependencies automatically)
ggx.sync(faq_pipeline)

```

---

## Best Practices

### ✅ Do's

1. **Always use the anchor comment**: `# -- BEGIN DEFINITION --`
2. **Validate groups exist**: Check your platform for valid group names before declaring
3. **Use type annotations**: Help the platform understand your data types
4. **Test locally first**: Run your functions before syncing to catch errors
5. **Use meaningful names**: Choose descriptive names for components
6. **Include the cache parameter**: Even if unused, include `cache: dict = {}`
7. **Write clear docstrings**: Document what each component does

### ❌ Don'ts

1. **Don't hardcode secrets**: Use environment variables for API keys and passwords
2. **Don't skip the cache parameter**: Required for all component functions
3. **Don't sync without testing**: Ensure functions work locally first
4. **Don't use undefined groups**: Verify group names exist on your platform instance
5. **Don't forget the anchor comment**: Missing anchor will cause sync errors

---

## Troubleshooting

### "Group not found" Warning

**Problem**: Warning message: `├ [WARN] Group "YourGroupName" not found: Ignoring the group`

**Cause**: The group specified in your declaration doesn't exist on the platform.

**Solution**:

- Check available groups in your platform UI
- Create the group in platform settings first
- Or remove the `group` parameter (it will default to None or the existing component's group)

**Note**: This is a warning, not an error - the sync will still complete successfully.

---

### "Expected anchor comment" Error

**Problem**: Error message: `AssertionError: Expected anchor comment # -- BEGIN DEFINITION -- to be present in source. Found None`

**Cause**: Your function is missing the required `# -- BEGIN DEFINITION --` anchor comment.

**Solution**: Add the anchor comment before your function's core logic:

```python
import genguardx as ggx
@ggx.Prompt.declare(name='My Prompt')
def my_prompt(*, cache: dict = {}, prompt: str = "Hello"):
    """Docstring here"""
    # -- BEGIN DEFINITION --  # <-- Add this line
    return prompt

```

---

### "Skipping X - not declared as a Corridor object" Warning

**Problem**: Warning message: `[WARN] Skipping "function_name" - as it is not declared as a Corridor object`

**Cause**: Your pipeline references a function that doesn't have a `@declare()` decorator.

**Solution**: Add the appropriate decorator to the referenced function:

```python
import genguardx as ggx
# Before (causes warning)
def helper_function():
    return "result"

# After (no warning)
@ggx.Prompt.declare(name='Helper')
def helper_function(*, cache: dict = {}, prompt: str = "result"):
    # -- BEGIN DEFINITION --
    return prompt

```

**Note**: This is a warning - the sync completes, but the dependency won't be tracked or synced.

---

### Invalid Metadata Values Warning

**Problem**: Warning messages like:

- `├ [WARN] Task Type "YourTaskType" is invalid: Ignoring the Task Type`
- `├ [WARN] Prompt Type "YourPromptType" is invalid: Ignoring the Prompt Type`

**Cause**: The value provided for a metadata parameter doesn't match the allowed values.

**Solution**: Check the Metadata Parameters Reference section above for the exact valid values. For example:

- Task Type must be one of: `'Classification'`, `'Question Answering'`, `'Information Extraction'`, etc.
- Prompt Type must be one of: `'System Instruction'`, `'User Prompt'`, `'Others'`

**Note**: This is a warning - the sync completes, but the invalid metadata field is ignored.

---

### "Prompt must be a kwarg named 'prompt'" Error

**Problem**: Error message: `ValueError: Prompt "your_prompt_name" must be a kwarg names: "prompt" which contains the prompt template as the default value`

**Cause**: Prompt functions require a specific parameter format.

**Solution**: Add `prompt: str = "your template"` as a keyword-only parameter:

```python
import genguardx as ggx
@ggx.Prompt.declare(name='My Prompt')
def my_prompt(*, cache: dict = {}, prompt: str = "Your prompt text here"):
    """Docstring"""
    # -- BEGIN DEFINITION --
    return prompt

```

---

### Type Hint Error for dict/list

**Problem**: Error message: `Unable to process type hint: '<class 'dict'>' as the dict has no inner type`

**Cause**: Using bare `dict` or `list` types without specifying inner types.

**Solution**: Use proper type hints with inner types:

```python
# Bad
context: dict = None

# Good
context: dict[str, str] = None
context: t.Optional[dict[str, str]] = None

# For lists
history: list = ()  # Bad
history: list[dict[str, str]] = ()  # Good

```

---

## Additional Resources

- **Platform Documentation**: Contact your platform administrator for instance-specific docs
- **API Reference**: Available in your GenGuardX instance
- **Support**: Contact your platform administrator or support team

---