# Azure
Source: https://docs.genguardx.ai/technology/self-hosting/installation/azure/
Markdown: https://docs.genguardx.ai/technology/self-hosting/installation/azure/index.md
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
4. Install Python 3.11, Java 8 for Spark, Nginx, and unzip.
5. Extract the GGX installation bundle.
6. Install the `app`, `api`, `worker-api`, `worker-spark`, and `jupyter` components.
7. Configure database and application settings.
8. Run database migrations.
9. Create systemd services and start the components.

Use Azure VMs when you need direct host access or your organization standardizes on VM operations. Use AKS or Azure Container Apps when you want managed container operations.

## Security Notes

- Use managed identities where possible.
- Store secrets in Key Vault or an approved secret store.
- Use private networking for PostgreSQL and storage.
- Enable encryption at rest for database and file storage.
- Restrict SSH access and use just-in-time access where available.
- Enable Azure Monitor and alerting before production rollout.