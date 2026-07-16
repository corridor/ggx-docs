# Kubernetes
Source: https://docs.genguardx.ai/technology/self-hosting/installation/kubernetes/
Markdown: https://docs.genguardx.ai/technology/self-hosting/installation/kubernetes/index.md
Description: Deploy self-hosted GGX on Kubernetes using Kustomize manifests, namespaces, persistent volumes, ingress, secrets, and provider-specific cluster settings.
Use Kubernetes when you want a cloud-native GGX deployment with managed rollout, namespace isolation, persistent volumes, and standard cluster operations.

GGX provides cloud-agnostic [GGX Kubernetes manifests](https://github.com/corridor/kubernetes-ggx). The manifests use Kustomize and can run on managed Kubernetes services including Azure Kubernetes Service (AKS), Google Kubernetes Engine (GKE), and Amazon Elastic Kubernetes Service (EKS).

## Deployment Shape

The Kubernetes deployment keeps the same GGX service split used by the other installation paths:

```text
Kubernetes cluster
├── ggx namespace
│   ├── corridor-app
│   ├── corridor-worker
│   └── corridor-jupyter
├── persistent volumes for data, uploads, notebooks, state, and backups
└── ingress routing / to corridor-app and /jupyter to corridor-jupyter
```

The `kubernetes-ggx` repository contains reusable manifests in `base/` and a deployable example overlay in `overlays/example/`. Create environment-specific overlays such as `overlays/prod`, `overlays/staging`, or separate team overlays when you need isolated deployments.

## Prerequisites

- A Kubernetes cluster with enough CPU, memory, and persistent storage for the [minimum requirements](../minimum-requirements/).
- `kubectl` access with permission to create namespaces, secrets, config maps, deployments, services, ingress resources, and persistent volume claims.
- GGX container registry credentials from GGX support.
- PostgreSQL metadata database connectivity.
- Persistent storage that supports the access pattern used by your deployment.
- DNS name and TLS certificate strategy for the public application endpoint.

## Quickstart

Create the namespace before creating namespace-scoped objects:

```bash
kubectl create namespace ggx
```

Create the image pull secret using the registry credential JSON provided by GGX:

```bash
kubectl create secret docker-registry corridor-registry-secret \
  --docker-server=us-central1-docker.pkg.dev \
  --docker-username=_json_key \
  --docker-password="$(cat /tmp/corridor-registry-key.json)" \
  --namespace ggx
```

Apply an overlay after you have reviewed and customized it:

```bash
kubectl apply -k overlays/example
```

Verify the rollout:

```bash
kubectl get pods -n ggx
kubectl get svc -n ggx
kubectl get ingress -n ggx
```

## Overlay Configuration

Before applying the overlay, configure the deployment for your environment:

- Set the GGX image tag in `overlays/example/kustomization.yaml`.
- Set the public hostname in `overlays/example/kustomization.yaml`.
- Set database, authentication, and application settings in `overlays/example/configs/api_config.py`.
- Update persistent volume claim patches if your cluster uses a different read-write-many storage class.
- Configure TLS secrets, ingress annotations, and timeout or gzip settings in the ingress manifest.
- Tune CPU and memory requests and limits in the service manifests.

## Provider Notes

### AKS

AKS deployments usually need:

- Azure RBAC permissions for AKS, virtual networks, managed identities, Azure Files, Azure Database for PostgreSQL, DNS, Key Vault, and Azure Monitor.
- Azure CNI or another networking mode approved by your platform team.
- Azure Files CSI Driver or an equivalent read-write-many storage provider.
- NGINX Ingress Controller or Application Gateway Ingress Controller.
- cert-manager or an Azure-managed certificate process.
- Network security group and database firewall rules allowing the cluster to reach PostgreSQL and shared storage.

Use the [Azure](../azure/) page for AKS-specific service choices and Terraform alternatives.

### GKE

GKE deployments usually need:

- IAM permissions for GKE, Compute Engine networking, Cloud SQL, Filestore or another RWX storage service, Secret Manager, Cloud DNS, and Cloud Monitoring.
- Required APIs enabled, including Kubernetes Engine, Compute Engine, Cloud SQL, and any storage or DNS APIs used by the deployment.
- Private cluster egress through Cloud NAT when worker nodes do not have public IPs.
- Filestore, another NFS provider, or a compatible RWX storage class for persistent volumes.
- Workload Identity if pods need direct access to Google Cloud services.
- Ingress and certificate configuration appropriate for your load balancer choice.

Use the [GCP](../gcp/) page for GKE-specific service choices and Terraform alternatives.

### EKS

EKS deployments usually need:

- IAM permissions for EKS, IAM, VPC, EC2, EFS, RDS, Elastic Load Balancing, ACM, Route 53, Secrets Manager, and CloudWatch.
- AWS Load Balancer Controller for ALB-backed ingress.
- EFS CSI Driver for read-write-many persistent volumes.
- IAM Roles for Service Accounts (IRSA) for controllers and any workload permissions.
- VPC CNI, Cilium, or another approved pod networking configuration.
- Security groups allowing cluster workloads to reach RDS, EFS mount targets, and any external dependencies.

Use the [AWS](../aws/) page for EKS-specific service choices and Terraform alternatives.

## Recommended Starting Cluster

| Provider | Cluster type | Starting nodes | Autoscaling | Node size | Disk | Notes |
|---|---|---:|---|---|---:|---|
| AKS | Standard | 1 | min 1, max 3 | `Standard_D8s_v3` | 100 GB | Use Azure CNI and approved virtual network |
| GKE | Standard | 1 | min 1, max 3 | `e2-standard-8` | 100 GB | Enable IP aliasing and approved VPC/subnet |
| EKS | Standard | 1 | min 1, max 3 | `m5.xlarge` or similar | 100 GB | Attach to approved VPC/subnet |

A single node is usually enough for proof-of-concept usage. Production deployments should size node pools, storage, database, and autoscaling limits based on expected user count, data volume, and background job concurrency.

## Operations

Common Kubernetes operations:

```bash
kubectl logs -n ggx deploy/corridor-app
kubectl logs -n ggx deploy/corridor-worker
kubectl exec -it -n ggx deploy/corridor-app -- /bin/bash
kubectl rollout restart deployment corridor-app -n ggx
kubectl rollout status deployment corridor-app -n ggx
kubectl get pvc -n ggx
```

If pods show `ImagePullBackOff`, check that `corridor-registry-secret` exists in the application namespace and contains the current registry credentials.