---
title: RAGs
---

<helper-panel object='Rag' location='list'>

## What is a RAG?

**Retrieval-Augmented Generation (RAG)** addresses the limitation that language models have fixed knowledge cutoffs and can't access current information. RAG systems retrieve relevant data from external sources in real-time, enabling models to provide up-to-date, factual responses grounded in current information.

Every RAG system in Corridor consists of three key components that work together to retrieve and process information:

![What is a RAG?](./rag-concept.excalidraw.svg)

- **Knowledge Source:** A repository of external information such as documents (PDFs, text files, CSVs), vector databases (like ChromaDB), graph databases (like Neo4j), or other structured/unstructured data sources
- **Initialization Logic:** Prepares the knowledge source or client for processing multiple retrieval requests, if needed
- **Scoring Logic:** Code that implements your retrieval strategy to find and return the most relevant information from the knowledge source based on input queries

Corridor supports registration of various RAG types to meet different use cases:

- **API-based:** Connect to external knowledge sources like vector databases, graph databases, and other APIs to retrieve information from external environments
- **Python-based:** Lightweight Python logic using various libraries or rule-based retrieval systems
- **Custom:** Upload knowledge files (CSV, text documents, PDFs) to create custom retrieval systems

## Managing RAGs in Corridor

The **RAG Registry** serves as a centralized location that organizes all registered RAGs into customized groups, enabling easier tracking, monitoring, and RAG creation across your organization.

## How to Register a RAG

### Basic Information
1. Navigate to **RAG Registry** and click **Create**
2. In the **Details** tab, provide a **Description** of your RAG, including its purpose, when to use it, and other relevant details
3. Click **Add Additional Details** to include supplementary information if needed

### RAG Configuration
4. In the **Code** section, configure the following:
   * **Alias**: Provide a variable name to refer to this RAG in Python definitions
   * **Output Type**: Specify the data type of the value returned by your RAG
   * **Input Type**: Select from three options:
     - **API Based**: For external knowledge sources (vector databases, graph databases, APIs)
     - **Python Function**: For lightweight Python logic or rule-based retrieval systems
     - **Custom**: For uploaded knowledge files (CSV, PDFs, etc)

### Arguments and Resources
5. **Define Arguments**: Add input parameters for your RAG
   * **Alias**: Variable name for the argument
   * **Type**: Data type of the input
   * **Is Optional**: Check if the argument is optional
   * **Default Value**: Provide default values for optional arguments
6. Click **Add Argument** to include additional input parameters
7. Click **Add Resources** to select registered resources (models, functions, prompts) to use in your RAG definition

### RAG Implementation
8. **For Custom type**: Upload your knowledge file using **Select file** or drag and drop
   * The uploaded knowledge files (CSV, PDFs, etc) that can be processed by vector databases or other retrieval systems can be accessed in Scoring Logic using the variable `knowledge` (type `pathlib.Path`)
9. **Write Scoring Logic** that:
    * Processes input arguments and retrieves relevant information
    * Accesses the knowledge source (uploaded file or external API)
    * Returns the retrieved and processed information

### Finalization
10. Use additional tools as needed:
    * **Format Code**: To properly format your Python code
    * **Test Code**: To validate your implementation
    * **requirements.txt**: To download Python dependencies information
11. Click **Create** to complete the registration process

Once registered, RAGs can be used in downstream objects such as models, pipelines, and reports.

## Benefits of RAG Registration

### Governance and Compliance
* **Automated tracking** and recording of modifications with efficient version control
* **Automatic detection** of Permissible Purpose violations
* **Transparent and fully auditable** journey to production with streamlined production monitoring

### Development and Testing
* **Testing and comparison** with other registered RAGs using custom and standardized validation kits
* **Extract ready-to-deploy executable artifacts** for production use
* **Fingerprinting** of external API connectivity for security and tracking

### Collaboration and Reusability
* **Enhanced reusability** across downstream applications and teams
* **Usage tracking** with comprehensive Lineage Tracking
* **Better collaboration** for continuous RAG development and testing
* **Centralized knowledge management** for improved information retrieval consistency

</helper-panel>