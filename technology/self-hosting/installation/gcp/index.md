# GCP
Source: https://docs.genguardx.ai/technology/self-hosting/installation/gcp/
Markdown: https://docs.genguardx.ai/technology/self-hosting/installation/gcp/index.md
Use this page to choose and configure a Google Cloud deployment path for GGX.

## Recommended GCP Paths

| Path | Use when | Primary docs |
|---|---|---|
| GKE | You already operate Kubernetes or need Kubernetes-native scaling and operations | [Kubernetes](../kubernetes/) |
| Cloud Run | You want Google-managed containers without managing a Kubernetes cluster | [Terraform](../terraform/) |
| Compute Engine VMs | You want a traditional VM-based install and direct OS control | [Manual](../manual/) |

## GKE-Specific Configuration

GKE uses the shared [GGX Kubernetes manifests](https://github.com/corridor/kubernetes-ggx). Start with the [Kubernetes](../kubernetes/) page, then apply the GCP-specific requirements below.

### Required GCP Services

- **Google Kubernetes Engine** for the managed Kubernetes cluster.
- **Cloud SQL for PostgreSQL** for GGX metadata.
- **Filestore** or another approved read-write-many storage provider.
- **VPC** with private networking for cluster, database, and storage connectivity.
- **Cloud NAT** when private nodes need outbound internet access.

Optional but common services:

- **Cloud DNS** for DNS.
- **Secret Manager** for sensitive configuration.
- **Cloud Monitoring and Cloud Logging** for observability.
- **Cloud Armor** for edge protection.
- **Cloud CDN** for static asset caching.

### Permissions

The deploying identity needs permission to manage:

- GKE clusters and node pools.
- VPC networks, subnets, firewall rules, routers, and Cloud NAT.
- Service accounts and IAM bindings.
- Cloud SQL instances, databases, and users.
- Filestore instances or the selected storage provider.
- Cloud DNS records and certificate resources when managed in GCP.
- Secret Manager secrets when application secrets are stored there.

Enable the required APIs before deployment, including Kubernetes Engine, Compute Engine, Cloud SQL, and any storage, DNS, certificate, or monitoring APIs used by your environment.

### Cluster Add-ons

Install or enable these before applying the GGX overlay:

- Ingress controller appropriate for your load balancer strategy.
- cert-manager if TLS is issued from the cluster.
- NFS or Filestore CSI/provisioning components for read-write-many volumes.
- Workload Identity if pods need direct access to Google Cloud services.
- Cloud Monitoring integration or another approved observability stack.

### Networking

Production GKE deployments should normally use private nodes with outbound internet through Cloud NAT. Firewall rules must allow:

- Ingress load balancer to reach `corridor-app` and `corridor-jupyter`.
- GGX pods to reach Cloud SQL.
- GGX pods to mount Filestore or the selected storage provider.
- Pods to pull GGX images from the configured registry.

## Cloud Run With Terraform

The [GGX Google Cloud Terraform module](https://github.com/corridor/terraform-google-ggx) deploys GGX on Cloud Run. This is the main non-Kubernetes GCP container path.

The module provisions or configures:

- `corridor-migration` as a Cloud Run Job.
- `corridor-app` as a public Cloud Run service.
- `corridor-worker` as an internal Cloud Run service with minimum instances.
- `corridor-jupyter` as a public Cloud Run service.
- Cloud SQL for PostgreSQL.
- Cloud Storage for shared file-backed state.
- Direct VPC egress from Cloud Run to private services.
- External HTTPS load balancer with serverless NEGs so `/` routes to the app and `/jupyter` routes to Jupyter.

Configure the module with the project ID, image, hostname, database password, license key, and SMTP values if email is required.

```bash
terraform init
terraform plan
terraform apply
```

After apply, point DNS at the reserved load balancer IP and wait for the managed certificate to become active.

## Compute Engine VM-Based Installs

A Compute Engine deployment follows the [Manual](../manual/) path. The Compute Engine installation pattern is:

1. Create a Compute Engine VM, commonly `n2-standard-8` or similar for all-in-one deployments.
2. Create Cloud SQL for PostgreSQL.
3. Install Python 3.11, Java 8 for Spark, Nginx, and unzip.
4. Extract the GGX installation bundle.
5. Install the `app`, `api`, `worker-api`, `worker-spark`, and `jupyter` components.
6. Configure database and application settings.
7. Run database migrations.
8. Create systemd services and start the components.

Use Compute Engine when you need direct host access or your organization standardizes on VM operations. Use GKE or Cloud Run when you want managed container operations.

## Security Notes

- Use service accounts with least-privilege IAM roles.
- Store secrets in Secret Manager or an approved secret store.
- Use private IP connectivity for Cloud SQL where possible.
- Enable encryption, automated backups, and monitoring.
- Restrict SSH access and prefer OS Login or IAP where available.
- Enable Cloud Logging and alerting before production rollout.