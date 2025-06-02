---
title: CICD & Direct to Production
---

Typically, production execution environments are kept separate and managed to ensure 100% uptime as these are mission-critical systems for organizations.

To tackle the air gap that these systems require - all analytics registered on the platform can be exported out from the system to be put into a Production Execution Environment. These production artifacts are locked to ensure they are not tampered with when they are promoted to production. And there is **NO extra dependency** required on the production side from Corridor - i.e. there is no requirement for a license key or a corridor installation in production!

The production artifact aims to:

- Extract the logic/items registered in Corridor - to then use it outside Corridor
- Self-sufficient with all information encapsulated in the artifact
- Have minimal dependencies on the runtime-environment where the artifact is run later

Typically a robust Continuous Deployment system is recommended to ensure that Governance is maintained while the production-artifacts are promoted. For example, you can use:

- Jenkins
- GitHub Actions
- AWS Code Pipelines
- Azure DevOps Pipelines
- Gitlab CICD
- CircleCI

And many others.

## Deploying as APIs

If the production system supports calling APIs - the production-artifact can also be wrapped using an API layer and exposed as a REST or SOAP API which can be called by the production system.

Typically the APIs should be considered state-less and any extra state management should be handled outside the API, but can be provided in the request payload of the API.

Production Artifacts can be deployed as APIs using containerized solutions like:

- Docker Compose
- Kubernetes
- AWS Elastic Container Service (ECS)
- AWS Elastic Kubernetes Service (EKS)
- AWS Fargate
- Pivotal Cloud Foundry
- Azure Container Instances
- Google Cloud Run
- Google Kubernetes Engine (GKE)
- VMWare TKGI

The API can also be deployed using application management solutions (server-based or serverless) like:

- AWS Beanstalk
- AWS Lambda
- Google App Engine (GAE)
- Google Functions
- Azure App Service
- Azure Functions

## Custom Production Setup

Not all production systems support running direct Python scripts or calling APIs - and some require providing specific GenAI components in a custom interface. To handle cases like this, while Robotic Process Automation (RPA) could be used - many times it is not worth the trouble that RPA brings with it.

Because of the transparency that Corridor's Inventory management provides, each part of the pipeline can be deployed independently.
For example:

- All the LLM configurations like `seed`, `temperature`, `top_k`, etc. can be extracted from the pipeline
- The prompt templates can be extracted and provided to the production system directly
- Knowledge files from RAGs can be locked and sent to production

## Internals of the Production Artifact

The artifact generated from the platform is independent of the platform and can run in an isolated runtime environment
or production environment. The information stored in the artifact is useful in many cases, where we might want to:

- check the metadata for the objects
- check the input tables and columns used
- see the lineage and relationship between the objects
- run the entire artifact or some components of the artifact to get complete or intermediate results

The artifact consists of the following files:

```none
model_a.b.c
├── metadata.json
├── input_info.json
├── ... (additional information about features etc. used)
├── python_dict
|     ├── __init__.py
|     ├── versions.json
|     └── Additional information
└── pyspark_dataframe
 ├── __init__.py
 ├── versions.json
 └── Additional information
```

The **metadata.json** contains metadata information about the folder it is in. It will have
information about the model, its inputs, its dependent variable, etc. It also has any other
metadata information registered in the platform like Groups, Permissible Purpose, etc.

The **versions.json** contains the versions of libraries that were used during the artifact
creation - python version, any ML libraries, etc.

The **input_info.json** contains the input data tables needed to be sent to the artifact's main() function.

The `__init__.py` file inside **pyspark_dataframe** and **python_dict** folders contain the end-to-end Python function
which can be used to run the entire artifact. They support different execution engines:

- Batch execution with PySpark (**pyspark_dataframe**)
- API execution in a Python environment (**python_dict**)

To run the artifact, simply call the `main()` function in the artifact with the needed data.  
The `python_dict/__init__.py` contains a `main()` function into which data can be sent - in the form of a  
python-dict for low-latency execution. A dataset in the dictionary format is described as a dict  
with type/values

## Using `corridor-runtime`

`corridor-runtime` is a utility package created by Corridor, which can help us in doing the above-mentioned tasks
in a very easy manner, without having to worry about extracting the artifact bundle (`bundle.tar.gz`) or the files
inside the bundle.
