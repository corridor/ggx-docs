---
title: "Deployment platforms"
description: "Choose where an approved agent can be deployed, turn platforms on or off for the organization or a project, and deploy to Databricks straight from GGX."
---

The **Deploy** dialog of an agent lists the platforms you can deploy it to. For each platform it shows the prerequisites and a set of example steps. The dialog fills in the exact commands for the agent, with its name and settings. This page covers what the platforms are and how administrators control which ones people can choose.

## How deploying works

1. Open the agent you want to deploy and choose **Deploy**.
2. Pick a platform. Filter by **Popular** or by category.
3. Follow the steps on the platform's page.

Record where the agent ends up under **Risk & Compliance → Deployments**. See [CI/CD and Direct to Production](../direct-to-production/).

## Platforms

GGX lists 75 platforms in five categories.

- **Hosting**: Alibaba Cloud, Amazon EC2, Amazon ECS (Fargate), Amazon EKS, AWS Lambda, Azure App Service, Azure Container Apps, Azure Functions, Azure Kubernetes Service, Cloudflare, Databricks Apps, DigitalOcean, Docker, Docker Compose, Fly.io, Google Cloud Run, Google Kubernetes Engine, HashiCorp Nomad, Heroku, Hugging Face Spaces, IBM Cloud Code Engine, Koyeb, Kubernetes, Linux VM, Northflank, OVHcloud, Podman, PythonAnywhere, Railway, Rancher, Red Hat OpenShift, Render, Replit, Scaleway, Snowflake Container Services, Vercel, Vultr
- **Agent runtimes**: Amazon Bedrock AgentCore Runtime, CrewAI AMP, Databricks Agent Runtime, Dify, IBM watsonx Orchestrate, LangSmith Deployment, Microsoft Foundry, Oracle OCI Generative AI, Salesforce Agentforce, Vertex AI Agent Engine
- **Model serving**: Amazon SageMaker, Anyscale, Baseten, BentoCloud, Cerebrium, Databricks Model Serving, Dataiku, DataRobot, Lightning AI, MLflow, Modal, NVIDIA, Palantir Foundry, Replicate, RunPod, SAP AI Core
- **Workflows**: Apache Airflow, Dagster, GitHub Actions, n8n, Prefect, Temporal, Zapier
- **Notebooks and apps**: Google Colab, Gradio, Jupyter, Python code, Streamlit

## Turn platforms on or off

Every platform is a row under **Deployment Platforms** in **Org Settings → Integrations**. Open a row and choose **Enabled** or **Disabled**.

- A platform disabled in **Org Settings** cannot be chosen in the Deploy dialog of any project.
- A project can also disable platforms for itself in **Project Settings → Integrations**. A platform disabled there cannot be chosen in the Deploy dialog of that project.
- If the organization disabled a platform, a project cannot enable it. The project dialog says so, and an organization admin can enable it again in Org Settings.
- Only organization admins can change the organization's platforms, and only project admins can change a project's.

## Deploy to Databricks from GGX

For most platforms GGX shows the steps and you run them. **Databricks Agent Runtime** can also be deployed from GGX itself.

### Set up the workspace

1. Open **Org Settings → Integrations → Deployment Platforms** and select **Databricks Agent Runtime**.
2. Under **Deploy from GGX**, enter the **Workspace URL**, such as `https://adb-1234.5.azuredatabricks.net`.
3. Choose how GGX signs in:
   - **Azure Managed Identity**, with an optional **Managed Identity Client ID** when the machine that runs GGX has several identities.
   - **OAuth client (M2M)**, with a **Client ID** and **Client Secret**.
   - **Access token**.
4. If the `databricks` command is not on the PATH of the GGX server, set the **Databricks CLI path**.
5. Select **Test connection**, then **Save**. The dialog then shows who GGX is signed in as.

The identity needs to create apps in the workspace. GGX deploys as that identity. Saved secrets and tokens are kept: leave the field empty to keep them.

### Deploy an agent

In the agent's **Deploy** dialog, choose **Databricks Agent Runtime**. Under **Deploy from GGX**:

- GGX builds the bundle and deploys it to the workspace your organization set. The app is named `agent-bricks-ggx-` followed by the agent's ID. If an app with that name exists in Databricks but GGX did not deploy it for this agent, GGX leaves it alone. Delete it in Databricks to deploy.
- The **Files of the app** view lets you edit, add, rename, or delete any file GGX generates. The deploy lays your changes over the generated files. You can compare a file with what GGX generates under **Changes**, and restore the generated file.
- **Server data** uploads data before each deploy: each server folder you add goes to its folder of a Volume, and files already there with the same size are kept. The section is hidden: right-click the **Deploy from GGX** heading to show it.
- Select **Deploy now**. A deploy takes several minutes. You can close the dialog: the deploy goes on. The dialog shows when it fails and keeps the output.
- To release a new version, select **Redeploy**. Redeploying restarts the app, so runs in progress fail and can be sent again.
- **Refresh** reloads the app's status. **Delete app** removes the app from Databricks.
