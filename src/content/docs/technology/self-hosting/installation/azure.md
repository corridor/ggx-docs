---
title: "Deploy GGX on Azure"
description: "Deploy self-hosted GGX on Azure using Container Apps, Azure Files, managed networking, database services with managed identity login, container registry, and Terraform."
---

Use this page to choose and configure an Azure deployment path for GGX.

## Recommended Azure Paths

| Path | Use when | Primary docs |
|---|---|---|
| AKS | You already operate Kubernetes or need Kubernetes-native scaling and operations | [Kubernetes](../kubernetes/) |
| Azure Container Apps | You want Azure-managed containers without managing a Kubernetes cluster | [Terraform](../terraform/) |
| Azure VMs | You want a traditional VM-based install and direct OS control | [Manual](../manual/) |

## AKS-Specific Configuration

AKS uses the shared [GGX Kubernetes manifests](https://github.com/corridor/kubernetes-ggx). Start with the [Kubernetes](../kubernetes/) page, then apply the Azure-specific requirements below.

### Required Azure Services

- **Azure Kubernetes Service** for the managed Kubernetes cluster.
- **Azure Database for PostgreSQL** for GGX metadata.
- **Azure Files Premium** or another approved read-write-many storage provider.
- **Azure Virtual Network** for private networking.
- **Azure DNS** or another DNS provider.

Optional but common services:

- **Azure Key Vault** for secrets.
- **Azure Monitor** for logs and metrics.
- **Azure Front Door** or Web Application Firewall for edge protection.
- **Application Gateway Ingress Controller** when your platform standardizes on Application Gateway.

### Permissions

The deploying identity needs permission to manage:

- AKS clusters and node pools.
- Virtual networks, subnets, route tables, private DNS zones, and network security groups.
- Managed identities and role assignments.
- Azure Files storage accounts and file shares.
- PostgreSQL servers, firewall rules, and private endpoints when used.
- DNS records and TLS certificate resources when managed in Azure.
- Key Vault secrets when application secrets are stored there.

### Cluster Add-ons

Install or enable these before applying the GGX overlay:

- Azure Files CSI Driver.
- NGINX Ingress Controller or Application Gateway Ingress Controller.
- cert-manager if TLS is issued from the cluster.
- Azure Monitor Container Insights or another approved observability stack.
- Network Policy if your environment requires pod-to-pod controls.

### Networking

Production AKS deployments should normally use controlled ingress and private connectivity to PostgreSQL and storage. Network security groups and database firewall rules must allow:

- Ingress controller to reach `corridor-app` and `corridor-jupyter`.
- GGX pods to reach Azure Database for PostgreSQL.
- GGX pods to mount Azure Files.
- Pods to pull GGX images from the configured registry.

## Azure Container Apps With Terraform

The [GGX Azure Terraform module](https://github.com/corridor/terraform-azurerm-ggx) deploys GGX on Azure Container Apps. This is the main non-Kubernetes Azure container path.

The module provisions or configures:

- Container Apps for the GGX app, worker, Jupyter, PostgreSQL-facing configuration, and Nginx routing.
- Azure Files for shared state.
- Optional dedicated workload profiles when higher memory or predictable capacity is required.
- Outputs for the app URL, Jupyter URL, Container App Environment, storage account, and database details.

Important inputs include the Azure region, ACR login server, ACR service principal credentials, image name, image version, GGX license key, database admin password, and optional workload profile.

```bash
terraform init
terraform plan
terraform apply
```

## Azure VM-Based Installs

An Azure VM deployment follows the [Manual](../manual/) path. The Azure VM installation pattern is:

1. Create a resource group and Azure VM, commonly `Standard_D8s_v3` or larger for an all-in-one deployment.
2. Attach and mount a data disk for `/opt/corridor` and application state.
3. Create Azure Database for PostgreSQL.
4. Install Python 3.11, Nginx, and unzip.
5. Extract the GGX installation bundle.
6. Install the `app`, `api`, `worker-api` (the [kernel worker](../../configurations/process-management/#kernel-runtime)), and `jupyter` components.
7. Configure database and application settings.
8. Run database migrations.
9. Create systemd services and start the components.

Use Azure VMs when you need direct host access or your organization standardizes on VM operations. Use AKS or Azure Container Apps when you want managed container operations.

## Database Login With A Managed Identity

On Azure, the platform can log in to the Metadata Database with a Microsoft Entra token of a managed identity instead of a password. This works for Azure Database for PostgreSQL and for Azure SQL.

Set the following in `api_config.py`:

```python
SQLALCHEMY_AZURE_MANAGED_IDENTITY = True
```

and give `SQLALCHEMY_DATABASE_URI` the database user of the identity and no password:

```python
# Azure Database for PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://<identity-name>@<server>.postgres.database.azure.com:5432/<database>'

# Azure SQL
SQLALCHEMY_DATABASE_URI = 'mssql://@<server>.database.windows.net/<database>?driver=ODBC+Driver+18+for+SQL+Server'
```

The platform uses the AKS workload identity when its variables are set (`AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_FEDERATED_TOKEN_FILE`, and `AZURE_AUTHORITY_HOST`, which the workload identity webhook sets in the pod), and the managed identity of the virtual machine otherwise. On a virtual machine, set `AZURE_CLIENT_ID` to the client ID of the identity that has the database user: without it, the token is the one of the machine's default identity, which has no login in the database. The tokens are renewed automatically.

The identity must exist as a user of the database. Create it with an administrator of Microsoft Entra on the server, and grant it the permissions the platform needs on the database.

For Azure SQL, the GGX image includes ODBC Driver 18 for SQL Server and unixODBC. The driver encrypts the connection: if the server uses a self-signed certificate, add `&TrustServerCertificate=yes` to the URI.

### Letting the ODBC driver log in (Azure SQL)

As an alternative, the ODBC driver can acquire the token by itself with the `authentication` keyword in the URI. Leave `SQLALCHEMY_AZURE_MANAGED_IDENTITY` off in this case. Write the keyword in lowercase: with `Authentication`, the connection also asks for Windows login, which the driver refuses.

- `authentication=ActiveDirectoryMSI`: an IMDS-based connection, which uses the managed identity of a VM, an App Service, and similar hosts through the instance metadata service.
- `authentication=ActiveDirectoryDefault`: a managed identity connection that follows the default credential chain: environment variables, workload identity, managed identity, and the Azure CLI.

```python
SQLALCHEMY_DATABASE_URI = 'mssql://@<server>.database.windows.net/<database>?driver=ODBC+Driver+18+for+SQL+Server&authentication=ActiveDirectoryMSI'
```

For a user-assigned managed identity, put its client ID as the user of the URI: `mssql://<client-id>@<server>.database.windows.net/<database>?...`.

## Container User And Shared Storage

The GGX containers run as UID 1001 in group 0, so the Azure Files share must be writable by group 0. See [Kubernetes](../kubernetes/#user-and-file-permissions) for the details.

## Security Notes

- Use managed identities where possible.
- Store secrets in Key Vault or an approved secret store.
- Use private networking for PostgreSQL and storage.
- Enable encryption at rest for database and file storage.
- Restrict SSH access and use just-in-time access where available.
- Enable Azure Monitor and alerting before production rollout.
