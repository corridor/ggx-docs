---
title: Model Catalog
---

<helper-panel object='FoundationModel' location='list'>

## What is a Model?

A model is a software program that uses algorithms or rules to make informed decisions, predictions, or generate responses based on input data without requiring explicit instructions for every scenario. Examples include machine learning models, lookup tables, if-else rules, and large language models (LLMs).

Every model in Corridor consists of three key components that work together to process inputs and generate outputs:

![What is a Model?](./model-concept.excalidraw.svg)

* **Model File**: Stores learned weights, parameters, lookup tables, tensors, and other data required to initialize the model
* **Initialization Logic**: Prepares the model or client for processing multiple inputs, if needed
* **Scoring Logic**: Code that processes inputs through the initialized model to generate predictions or responses

## Supported Model Types

Corridor supports registration of various model types to meet different use cases:

* **API-based models**: Connect to externally hosted models like OpenAI, Gemini, and Claude using APIs
* **Python-based models**: Lightweight Python logic using various libraries or rule-based models
* **Custom models**: Uploaded model files, including Scikit-learn models, NLP models like BERT, and fine-tuned models

## Managing Models in the Model Catalog

The **Model Catalog** serves as a centralized location that organizes all registered models into customized groups, enabling easier tracking, monitoring, and model creation across your organization.

## How to Register a Model

### Basic Information
1. Navigate to **Model Catalog** and click **New Model**
2. In the **Details** tab, provide a **Description** of your model, including how to use it, when it should be used, and when it should not be used
3. Click **Add Additional Details** to include supplementary information if needed

### Model Configuration
4. In the **Code** section, configure the following:
   * **Alias**: Provide a variable name to refer to this object in Python definitions
   * **Output Type**: Specify the data type of the value returned by your model
   * **Input Type**: Select from three options:
     - **API Based**: For externally hosted models (OpenAI, Gemini, Claude, etc.)
     - **Python Function**: For lightweight Python logic or rule-based models  
     - **Custom**: For uploaded model files (Scikit-learn, BERT, fine-tuned models, etc.)

### Arguments and Resources
5. **Define Arguments**: Add input parameters for your model
   * **Alias**: Variable name for the argument
   * **Type**: Data type of the input
   * **Is Optional**: Check if the argument is optional
   * **Default Value**: Provide default values for optional arguments
6. Click **Add Argument** to include additional input parameters
7. Click **Add Resources** to select registered resources (models, functions, prompts) to use in your model definition

### Model Implementation
8. **For Python Function and Custom types**: Write your logic in the code editor provided
9. **For Custom type**: Upload your model file using **Select file** or drag and drop
   * The uploaded file can be accessed in Scoring Logic using the variable `model` (type `pathlib.Path`)
10. **Model Provider**: For API-based models, select your API provider from the dropdown

### Finalization
11. Use additional tools as needed:
    * **Format Code**: To properly format your Python code
    * **Test Code**: To validate your implementation
    * **requirements.txt**: To specify Python dependencies
12. **Save** your model to complete the registration process

Once registered, models can be evaluated directly in the Model Catalog or used in downstream objects such as RAG systems, pipelines, and reports.

## Benefits of Model Registration

### Governance and Compliance
* **Automated tracking** and recording of modifications with efficient version control
* **Automatic detection** of Permissible Purpose violations
* **Transparent and fully auditable** journey to production
* **Production monitoring** becomes streamlined and efficient

### Development and Testing
* **Testing and comparison** with other registered models using custom and standardized validation kits
* **Extract ready-to-deploy executable artifacts** for production use
* **Fingerprinting** of external API connectivity for security and tracking

### Collaboration and Reusability
* **Enhanced reusability** across downstream applications and teams
* **Usage tracking** with comprehensive Lineage Tracking
* **Better collaboration** for continuous model building and testing
* **Centralized model management** for improved team coordination

</helper-panel>