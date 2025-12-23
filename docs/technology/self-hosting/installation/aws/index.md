---
title: Install on Amazon Web Services (AWS)
---

This guide provides an overview of deploying Corridor on Amazon Web Services. Corridor supports three deployment approaches on AWS.

## Use Cases

Corridor GenGuardX is a Responsible AI Governance & Testing Automation Platform designed to help organizations deploy and manage Generative AI applications securely and compliantly. Common use cases include:

- **IVR Systems**: Deploy and monitor interactive voice response systems powered by GenAI
- **Agent Assist Tools**: Build and govern AI-powered customer service agent assistance applications
- **Chatbots**: Create, test, and deploy conversational AI chatbots with comprehensive governance
- **RAG Applications**: Deploy Retrieval-Augmented Generation systems with end-to-end testing and monitoring
- **Multi-Agent Workflows**: Orchestrate complex agent-based workflows with approval and monitoring capabilities
- **Regulatory Compliance**: Ensure GenAI applications meet Model Risk Management (MRM), Fair Lending, and other regulatory requirements

Corridor enables organizations to move from experimentation to production deployment of high-ROI GenAI use cases with strong end-to-end pipeline testing, regulatory governance, and continual human-in-the-loop monitoring.

## Technical Prerequisites and Requirements

Before beginning the deployment, ensure the following technical prerequisites and requirements are met:

### Operating System Requirements

- **EC2 Deployments**: Amazon Linux 2, Ubuntu 20.04 LTS or later, or RHEL 8+ for EC2-based installations
- **EKS/ECS Deployments**: Container-based deployments use Linux-based container images (no OS installation required on host)
- **Python**: Python 3.11+ is required for EC2 deployments
- **Java**: Java 8+ is required for Spark worker functionality (EC2 deployments)

### Database Requirements

- **Database Type**: PostgreSQL 11.7+ (PostgreSQL 14+ recommended for production)
- **Database Storage**: Minimum 5 GB for metadata storage (production deployments should allocate 100 GB+)
- **Database Configuration**: 
  - Multi-AZ configuration recommended for production environments
  - Automated backups enabled
  - Encryption at rest enabled
- **Alternative Databases**: Oracle 19+ or MSSQL 2016+ are supported but PostgreSQL is recommended for AWS deployments

### Storage Requirements

- **File Storage**: Minimum 50 GB for file management (production deployments should allocate 500 GB+)
- **Storage Types**:
  - **EKS/Fargate**: Amazon EFS (Elastic File System) for persistent storage
  - **EC2**: EBS volumes (gp3 recommended) or Amazon S3 for object storage
- **Database Storage**: EBS-backed storage for RDS instances (gp3 or io1/io2 for high-performance workloads)
- **Backup Storage**: Amazon S3 for database backups and snapshots

### Compute Requirements

- **Web Application & API Worker**: Minimum 4 GB RAM, 4 CPU cores
- **Spark Worker**: Minimum 16 GB RAM, 8 CPU cores (for data processing workloads)
- **Jupyter Notebook**: Minimum 4 GB RAM, 4 CPU cores (scales with concurrent users)
- **Redis**: Minimum 1 GB RAM, 1 CPU core
- **Database (RDS)**: Minimum db.t3.medium (2 vCPU, 4 GB RAM) for development; db.t3.xlarge+ recommended for production

### Network Requirements

- **VPC**: Virtual Private Cloud with public and private subnets
- **Subnets**: Minimum 2 availability zones for production deployments
- **Internet Connectivity**: NAT Gateway for outbound internet access from private subnets
- **DNS**: Domain name system (DNS) configuration via Route 53 or external DNS provider
- **SSL/TLS**: SSL certificates for HTTPS (Let's Encrypt via cert-manager or AWS Certificate Manager)

### AWS Service Quotas

Ensure sufficient service quotas (limits) are available in your AWS account:
- EC2 instances (if using EC2 deployment)
- EKS clusters and nodes (if using EKS deployment)
- ECS tasks and services (if using Fargate deployment)
- RDS instances
- EFS file systems
- VPCs and subnets
- NAT Gateways
- Application Load Balancers

For detailed component-specific requirements, refer to the [Minimum Requirements](../minimum-requirements.md) documentation.

## Prerequisite Skills or Specialized Knowledge

Successful deployment of Corridor on AWS requires familiarity with the following skills and knowledge areas:

### AWS Knowledge

- **AWS Fundamentals**: Understanding of AWS core services, regions, availability zones, and account management
- **AWS Networking**: Knowledge of VPC, subnets, security groups, route tables, NAT Gateways, and Internet Gateways
- **AWS IAM**: Understanding of IAM roles, policies, and service roles for resource access
- **AWS Compute Services**: Familiarity with at least one of the following:
  - **EKS**: Kubernetes concepts, EKS cluster management, node groups, and Kubernetes resource management
  - **ECS**: ECS clusters, task definitions, services, and Fargate launch types
  - **EC2**: EC2 instance management, AMIs, security groups, and instance types

### AWS Services Knowledge

Deployers should be familiar with the following AWS services used in Corridor deployments:

- **Amazon RDS**: Database instance creation, configuration, Multi-AZ setup, and backup management
- **Amazon EFS**: File system creation, mount targets, and access point configuration (for EKS/Fargate)
- **Amazon S3**: Bucket creation, IAM policies, and object storage management
- **Application Load Balancer**: ALB configuration, target groups, listeners, and SSL certificate management
- **Route 53**: DNS zone management, record creation, and health checks
- **AWS Secrets Manager**: Secret storage and retrieval for sensitive configuration
- **CloudWatch**: Logging, monitoring, and alerting configuration
- **AWS WAF**: Web application firewall rules and DDoS protection (optional)

### Scripting and Programming Languages

- **Bash/Shell Scripting**: Required for automation scripts, installation procedures, and system administration tasks
- **Python**: Python 3.11+ knowledge is helpful for troubleshooting and custom configuration (EC2 deployments)
- **Terraform or CloudFormation**: Infrastructure-as-Code (IaC) knowledge is recommended for automated deployments
- **YAML/JSON**: Understanding of YAML and JSON syntax for configuration files (Kubernetes manifests, ECS task definitions, etc.)

### Additional Skills (by Deployment Method)

**For EKS Deployments:**
- **Kubernetes**: Strong understanding of Kubernetes concepts including pods, services, deployments, ConfigMaps, Secrets, and Ingress
- **kubectl**: Proficiency with kubectl command-line tool
- **eksctl**: Familiarity with eksctl for EKS cluster management (optional but recommended)
- **Kustomize or Helm**: Knowledge of Kubernetes package management tools

**For ECS Fargate Deployments:**
- **Docker**: Understanding of container concepts and Docker images
- **ECS CLI**: Basic familiarity with ECS command-line tools

**For EC2 Deployments:**
- **Linux System Administration**: SSH access, package management, service management (systemd), and file system operations
- **Network Configuration**: Understanding of network interfaces, firewall rules, and routing

### Recommended Experience Level

- **Minimum**: 1-2 years of AWS experience with hands-on deployment experience
- **Recommended**: 3+ years of AWS experience with production deployment experience
- **For EKS**: Additional 1+ years of Kubernetes experience

## Environment Configuration

Before deploying Corridor, ensure the following environment configuration is in place:

### AWS Account Requirements

- **Active AWS Account**: A valid AWS account with appropriate billing and payment methods configured
- **IAM Permissions**: AWS account or IAM user with sufficient permissions to create and manage:
  - EC2 instances, EKS clusters, or ECS clusters (depending on deployment method)
  - RDS database instances
  - VPC, subnets, security groups, and networking resources
  - EFS file systems or S3 buckets
  - Application Load Balancers
  - IAM roles and policies
  - Route 53 hosted zones (if using Route 53)
  - CloudWatch logs and metrics
- **Service Quotas**: Verify that AWS service quotas (limits) are sufficient for your deployment size
- **Billing Alerts**: Configure AWS billing alerts to monitor costs

### Operating System Configuration

- **EC2 Deployments**: 
  - EC2 instances must be launched with a supported AMI (Amazon Linux 2, Ubuntu 20.04+, or RHEL 8+)
  - SSH access configured with key pairs or AWS Systems Manager Session Manager
  - System updates applied and security patches installed
- **EKS/ECS Deployments**: 
  - No OS configuration required on host systems (container-based)
  - Container images must be based on Linux

### Licensing Requirements

- **Corridor Software**: Valid Corridor license and access to Corridor installation bundle or container images
- **Container Registry Access**: Access credentials for Corridor container registry (for EKS/ECS deployments)
- **Third-Party Software**: 
  - PostgreSQL database (managed by AWS RDS - no separate license required)
  - Redis (open-source, no license required)
  - Python 3.11+ (open-source)
  - Java 8+ (open-source OpenJDK)
  - Spark 3.3+ (open-source, if using Spark workers)

### DNS Configuration

- **Domain Name**: A registered domain name for accessing the Corridor instance (e.g., `corridor.example.com`)
- **DNS Provider**: Either:
  - **AWS Route 53**: Hosted zone configured in Route 53
  - **External DNS Provider**: DNS provider (e.g., Cloudflare, GoDaddy) with ability to create A and CNAME records
- **DNS Records**: Ability to create DNS records pointing to the Application Load Balancer
- **SSL Certificate**: SSL/TLS certificate for HTTPS (can be obtained via Let's Encrypt or AWS Certificate Manager)

### Network Configuration

- **VPC Setup**: 
  - VPC with CIDR block (e.g., 10.0.0.0/16)
  - Public subnets for load balancers and NAT Gateways
  - Private subnets for application components and databases
  - Minimum 2 availability zones for production deployments
- **Security Groups**: Security group rules configured for:
  - Application Load Balancer (inbound HTTPS/HTTP from internet)
  - Application components (inbound from ALB, outbound to internet)
  - Database (inbound from application components only)
  - EFS mount targets (inbound from application components)
- **NAT Gateway**: NAT Gateway configured in public subnet for outbound internet access from private subnets

### Access and Authentication

- **AWS CLI**: AWS CLI installed and configured with appropriate credentials
- **kubectl** (EKS only): kubectl CLI installed and configured to access EKS cluster
- **eksctl** (EKS only, optional): eksctl CLI installed for EKS cluster management
- **SSH Access** (EC2 only): SSH key pair created and configured for EC2 instance access
- **Container Registry**: Access credentials configured for pulling Corridor container images (EKS/ECS deployments)



## Security Configuration

This section provides comprehensive security guidance for deploying Corridor on AWS, including access controls, encryption, network security, and data protection measures.

### AWS Account Root User Warning

!!! warning "Do Not Use AWS Account Root User"

    **CRITICAL SECURITY REQUIREMENT**: The Corridor deployment and operation **must not** require the use of AWS account root user credentials. Using the root account for deployment or operations poses significant security risks.

    **Required Actions:**
    - Create IAM users or roles with appropriate permissions for deployment and operations
    - Never use root account credentials for day-to-day operations
    - Enable MFA (Multi-Factor Authentication) on the root account and store credentials securely
    - Use the root account only for initial account setup and critical account-level operations

    For more information on securing your root account, refer to the [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#lock-away-credentials) documentation.

### Principle of Least Privilege

All IAM roles, policies, and access configurations must follow the **principle of least privilege**, granting only the minimum permissions necessary for each component to function.

**Guidance for IAM Roles and Policies:**

- **EKS Cluster Service Role**: Grants permissions for EKS to create and manage AWS resources on your behalf
  - Required permissions: `eks:CreateCluster`, `eks:DescribeCluster`, `ec2:CreateNetworkInterface`, `ec2:DescribeNetworkInterfaces`
  - Should NOT include: Full EC2 access, S3 write access, or other unnecessary permissions

- **EKS Node Group Role**: Allows EKS nodes to join the cluster and access required AWS services
  - Required permissions: `ec2:DescribeInstances`, `ec2:DescribeInstanceTypes`, `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`
  - Should NOT include: S3 write access (unless specifically required), RDS access, or other unrelated services

- **ECS Task Execution Role**: Allows ECS tasks to pull container images and write logs
  - Required permissions: `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, `logs:CreateLogStream`, `logs:PutLogEvents`
  - Should NOT include: S3 access, RDS access, or other unnecessary permissions

- **ECS Task Role**: Grants permissions for application code running in containers
  - Should be scoped to only the specific AWS services the application needs (e.g., S3 read/write for specific buckets, Secrets Manager read for specific secrets)
  - Should NOT include: Broad S3 access, RDS admin access, or other overly permissive policies

- **EC2 Instance Profile**: For EC2 deployments, grants permissions for the instance to access AWS services
  - Should be scoped to only required services (e.g., S3 read/write for specific buckets, Secrets Manager read)
  - Should NOT include: Full EC2 access, RDS admin access, or other unnecessary permissions

**Best Practices:**
- Review and audit IAM policies regularly
- Use AWS IAM Policy Simulator to test permissions before deployment
- Implement resource-level permissions (e.g., restrict S3 access to specific buckets)
- Use condition keys to further restrict access (e.g., IP address restrictions, time-based access)
- Separate read and write permissions where possible
- Document the purpose of each permission granted

### Public Resources Documentation

Corridor deployments on AWS are designed to minimize public exposure. The following resources may be configured as public:

**Public Resources:**

- **Application Load Balancer (ALB)**: The ALB is deployed in public subnets and accepts inbound HTTPS/HTTP traffic from the internet. This is required for users to access the Corridor web interface.
  - **Security**: ALB should be configured with security groups that only allow HTTPS (port 443) and optionally HTTP (port 80) for redirects
  - **Recommendation**: Use AWS WAF in front of the ALB for additional protection

- **Route 53 Public Hosted Zone** (if using Route 53): Public DNS records are required for domain resolution
  - **Security**: DNS records themselves are public by design; ensure DNS records point to the ALB, not directly to application instances

**Private Resources (Not Publicly Accessible):**

- **EC2 Instances**: Deployed in private subnets, not directly accessible from the internet
- **EKS Nodes**: Deployed in private subnets
- **ECS Tasks**: Deployed in private subnets
- **RDS Database**: Deployed in private subnets, accessible only from application components
- **EFS File Systems**: Mount targets in private subnets, accessible only from application components
- **S3 Buckets**: By default, S3 buckets are private. Bucket policies should NOT allow public access unless specifically required for a use case (which is not typical for Corridor deployments)

**No Public S3 Buckets Required**: Corridor deployments do not require any S3 buckets with public access policies. All S3 buckets used for file storage, backups, or other purposes should be configured as private with appropriate IAM policies for access control.

### IAM Roles and Policies Purpose

The following IAM roles and policies are created during Corridor deployment. Each role serves a specific purpose:

**EKS Deployments:**

- **EKS Cluster Service Role** (`AmazonEKSClusterPolicy`, `AmazonEKSVPCResourceController`)
  - **Purpose**: Allows the EKS service to create and manage AWS resources (VPC, ENIs, security groups) on your behalf
  - **Used by**: EKS service when creating/managing the cluster
  - **Scope**: Cluster-level operations

- **EKS Node Group Role** (`AmazonEKSWorkerNodePolicy`, `AmazonEKS_CNI_Policy`, `AmazonEC2ContainerRegistryReadOnly`, `AmazonEKS_EFS_CSI_Driver_Policy`)
  - **Purpose**: Allows EKS worker nodes to join the cluster, pull container images from ECR, and access EFS for persistent storage
  - **Used by**: EC2 instances in the EKS node group
  - **Scope**: Node-level operations

- **EKS Pod Service Account Role** (Application-specific)
  - **Purpose**: Grants permissions for application pods to access AWS services (S3, Secrets Manager, etc.)
  - **Used by**: Corridor application containers running in pods
  - **Scope**: Application-level operations, scoped to specific services and resources

**ECS Fargate Deployments:**

- **ECS Task Execution Role** (`AmazonECSTaskExecutionRolePolicy`)
  - **Purpose**: Allows ECS tasks to pull container images from ECR and write logs to CloudWatch
  - **Used by**: ECS service when starting tasks
  - **Scope**: Task lifecycle operations

- **ECS Task Role** (Application-specific)
  - **Purpose**: Grants permissions for application code running in containers to access AWS services
  - **Used by**: Corridor application containers
  - **Scope**: Application runtime operations, scoped to specific services

**EC2 Deployments:**

- **EC2 Instance Profile Role** (Application-specific)
  - **Purpose**: Grants permissions for the EC2 instance to access AWS services (S3, Secrets Manager, CloudWatch)
  - **Used by**: Corridor application components running on the EC2 instance
  - **Scope**: Instance-level operations

**Common Policies:**

- **Secrets Manager Read Policy**: Allows reading specific secrets from AWS Secrets Manager
  - **Purpose**: Retrieve database credentials and other sensitive configuration
  - **Scope**: Read-only access to specific secret ARNs

- **S3 Access Policy**: Allows read/write access to specific S3 buckets
  - **Purpose**: Store and retrieve files, backups, and artifacts
  - **Scope**: Bucket-level or object-level permissions

### Keys Purpose and Location

The following keys and credentials are created or used during Corridor deployment:

**SSH Key Pairs (EC2 Deployments Only):**

- **Purpose**: Secure access to EC2 instances for initial setup and troubleshooting
- **Location**: 
  - Public key: Stored in AWS EC2 Key Pairs service, associated with EC2 instances
  - Private key: Stored securely on the deployer's local machine (never stored in AWS)
- **Usage**: Used for SSH access to EC2 instances
- **Security**: Private keys should be stored with appropriate file permissions (chmod 600) and never shared or committed to version control

**Database Credentials:**

- **Purpose**: Authentication to the RDS PostgreSQL database
- **Location**: 
  - **Primary Storage**: AWS Secrets Manager (recommended)
  - **Alternative**: Environment variables or configuration files (less secure)
- **Usage**: Used by Corridor application components to connect to the database
- **Security**: 
  - Rotate credentials regularly (every 90 days recommended)
  - Use Secrets Manager for automatic rotation if possible
  - Never hardcode credentials in application code or configuration files

**Container Registry Credentials (EKS/ECS Deployments):**

- **Purpose**: Authentication to pull Corridor container images from the container registry
- **Location**: 
  - **EKS**: Stored as Kubernetes image pull secrets in the cluster
  - **ECS**: Stored in ECS task definition or retrieved via IAM role (if using ECR)
- **Usage**: Used by Kubernetes/ECS to authenticate and pull container images
- **Security**: 
  - Use IAM roles for ECR access when possible (no credentials needed)
  - If using external registries, store credentials in AWS Secrets Manager

**SSL/TLS Certificates:**

- **Purpose**: Encrypt HTTPS traffic between users and the application
- **Location**: 
  - **EKS**: Managed by cert-manager, stored as Kubernetes secrets
  - **ECS/EC2**: AWS Certificate Manager (ACM) or Let's Encrypt certificates
- **Usage**: Used by Application Load Balancer for SSL/TLS termination
- **Security**: Certificates are automatically renewed by cert-manager or ACM

**API Keys and Application Secrets:**

- **Purpose**: Authentication for external integrations (LLM providers, data sources, etc.)
- **Location**: AWS Secrets Manager (recommended) or environment variables
- **Usage**: Used by Corridor application components for external API access
- **Security**: Rotate regularly and use Secrets Manager for centralized management

### Secrets Management

Corridor deployments use AWS Secrets Manager for secure storage and management of sensitive credentials and configuration.

**Secrets Stored in AWS Secrets Manager:**

- **Database Credentials**: RDS PostgreSQL username and password
- **Application Secrets**: API keys, tokens, and other sensitive configuration
- **External Integration Credentials**: LLM provider API keys, data source credentials

**Maintaining Stored Secrets:**

1. **Initial Secret Creation**:
   ```bash
   # Create database credentials secret
   aws secretsmanager create-secret \
     --name corridor/database/credentials \
     --secret-string '{"username":"corridor","password":"<secure-password>"}'
   ```

2. **Secret Rotation**:
   - **Manual Rotation**: Update secrets via AWS Secrets Manager console or CLI
   - **Automatic Rotation**: Configure RDS automatic password rotation (if supported)
   - **Rotation Schedule**: Rotate secrets every 90 days or as per organizational policy

3. **Secret Access**:
   - Application components retrieve secrets at runtime via AWS SDK
   - Never log or expose secret values in application logs
   - Use IAM policies to restrict secret access to specific roles/users

4. **Secret Updates**:
   - Update secrets via AWS Secrets Manager console or CLI
   - Application components should handle secret updates gracefully (may require restart)
   - Test secret updates in non-production environments first

5. **Secret Deletion**:
   - Use recovery window (7-30 days) when deleting secrets
   - Ensure applications are updated before permanently deleting secrets
   - Document all secrets and their purposes

**Best Practices:**
- Use separate secrets for different environments (dev, staging, production)
- Implement secret versioning to track changes
- Monitor secret access via CloudTrail
- Use resource-based policies to restrict secret access
- Regularly audit secret access permissions

### Sensitive Customer Data Storage

Corridor stores customer data in the following locations. All storage locations implement encryption at rest and in transit:

**Database Storage (Amazon RDS PostgreSQL):**

- **Location**: RDS PostgreSQL database instance
- **Data Stored**: 
  - User account information (usernames, email addresses, hashed passwords)
  - Application metadata (pipelines, prompts, models, RAG configurations)
  - Evaluation results and reports
  - Audit logs and activity history
- **Encryption**: Encryption at rest enabled (AWS KMS), encryption in transit (TLS)
- **Access Control**: Database accessible only from application components via security groups and IAM authentication

**File Storage (Amazon EFS or EBS):**

- **Location**: 
  - **EKS/Fargate**: Amazon EFS file system
  - **EC2**: EBS volumes attached to EC2 instances
- **Data Stored**: 
  - Uploaded files and datasets
  - Generated artifacts and outputs
  - Temporary files and cache
- **Encryption**: Encryption at rest enabled (AWS KMS for EFS, EBS encryption for volumes), encryption in transit (TLS for EFS)
- **Access Control**: File systems accessible only from application components via security groups and mount targets

**Object Storage (Amazon S3):**

- **Location**: Amazon S3 buckets (optional, for backups and large files)
- **Data Stored**: 
  - Database backups and snapshots
  - Large files and datasets
  - Exported reports and artifacts
- **Encryption**: Server-side encryption enabled (SSE-S3 or SSE-KMS), encryption in transit (HTTPS)
- **Access Control**: Buckets are private; access controlled via IAM policies and bucket policies

**Application Memory (Temporary):**

- **Location**: Application server memory (Redis, application cache)
- **Data Stored**: 
  - Session data
  - Temporary task data
  - Cache entries
- **Encryption**: Data in memory is not encrypted (standard for in-memory storage)
- **Access Control**: Redis accessible only from application components via security groups

**Log Storage (Amazon CloudWatch Logs):**

- **Location**: CloudWatch Logs
- **Data Stored**: 
  - Application logs
  - Access logs
  - Error logs
- **Encryption**: Encryption at rest enabled (AWS KMS), encryption in transit (TLS)
- **Access Control**: Log groups accessible only via IAM policies

**Data Residency**: Customer data remains within the selected AWS region unless explicitly configured for cross-region replication (backups only).

### Data Encryption Configurations

Corridor deployments implement encryption at rest and in transit for all data storage and communication:

**Encryption at Rest:**

- **Amazon RDS PostgreSQL**:
  - **Encryption Method**: AWS KMS (Key Management Service) encryption
  - **Configuration**: Encryption enabled during RDS instance creation
  - **Key Management**: Customer-managed KMS keys (CMK) or AWS-managed keys
  - **Scope**: All database data, logs, backups, and snapshots

- **Amazon EFS**:
  - **Encryption Method**: AWS KMS encryption
  - **Configuration**: Encryption enabled during EFS file system creation
  - **Key Management**: Customer-managed KMS keys (CMK) or AWS-managed keys
  - **Scope**: All files stored in EFS

- **Amazon EBS Volumes** (EC2 deployments):
  - **Encryption Method**: EBS encryption using AWS KMS
  - **Configuration**: Encryption enabled during volume creation or via instance-level encryption
  - **Key Management**: Customer-managed KMS keys (CMK) or AWS-managed keys
  - **Scope**: All data on EBS volumes, including root volumes and data volumes

- **Amazon S3**:
  - **Encryption Method**: Server-Side Encryption (SSE-S3 or SSE-KMS)
  - **Configuration**: Default encryption enabled on S3 buckets
  - **Key Management**: AWS-managed keys (SSE-S3) or customer-managed KMS keys (SSE-KMS)
  - **Scope**: All objects stored in S3 buckets

- **Amazon CloudWatch Logs**:
  - **Encryption Method**: AWS KMS encryption
  - **Configuration**: Encryption enabled on log groups
  - **Key Management**: Customer-managed KMS keys (CMK) or AWS-managed keys
  - **Scope**: All log data stored in CloudWatch Logs

**Encryption in Transit:**

- **HTTPS/TLS**: All communication between users and the application is encrypted using TLS 1.2 or higher
  - **SSL/TLS Termination**: Application Load Balancer handles SSL/TLS termination
  - **Certificate Management**: Certificates managed via AWS Certificate Manager (ACM) or Let's Encrypt (via cert-manager)

- **Database Connections**: All connections to RDS PostgreSQL are encrypted using TLS
  - **Configuration**: TLS required in database connection strings
  - **Certificate Validation**: RDS SSL certificates validated

- **EFS Connections**: All connections to EFS are encrypted using TLS
  - **Configuration**: TLS encryption enabled for EFS mount operations

- **S3 Connections**: All connections to S3 use HTTPS
  - **Configuration**: S3 endpoints use HTTPS by default

- **Internal Communication**: Application components communicate over encrypted channels within the VPC

**Key Management:**

- **AWS KMS**: Use AWS Key Management Service for managing encryption keys
- **Key Rotation**: Enable automatic key rotation for KMS keys (annual rotation)
- **Key Access**: Restrict KMS key access via IAM policies following least privilege principles
- **Audit**: Monitor key usage via CloudTrail

### Network Configuration Details

Corridor deployments involve multiple network components working together to provide secure, isolated networking:

**Virtual Private Cloud (VPC):**

- **Purpose**: Provides isolated network environment for Corridor resources
- **Configuration**: 
  - CIDR block: Typically 10.0.0.0/16 (65,536 IP addresses)
  - DNS resolution and DNS hostnames enabled
  - Internet gateway attached for public subnet internet access
- **Location**: Single AWS region (multi-region deployments use separate VPCs per region)

**Subnets:**

- **Public Subnets**: 
  - **Purpose**: Host Application Load Balancer and NAT Gateways
  - **Configuration**: 
    - CIDR blocks: e.g., 10.0.1.0/24, 10.0.2.0/24 (one per availability zone)
    - Route table: Routes internet traffic (0.0.0.0/0) to Internet Gateway
    - Auto-assign public IP: Enabled
  - **Location**: Minimum 2 availability zones for high availability

- **Private Subnets**: 
  - **Purpose**: Host application components, databases, and internal resources
  - **Configuration**: 
    - CIDR blocks: e.g., 10.0.10.0/24, 10.0.11.0/24 (one per availability zone)
    - Route table: Routes internet traffic (0.0.0.0/0) to NAT Gateway
    - Auto-assign public IP: Disabled
  - **Location**: Minimum 2 availability zones for high availability

**Security Groups:**

- **ALB Security Group**:
  - **Inbound Rules**: 
    - HTTPS (443) from 0.0.0.0/0 (internet)
    - HTTP (80) from 0.0.0.0/0 (for redirects to HTTPS)
  - **Outbound Rules**: 
    - All traffic to application security group (ports 80, 443)
  - **Purpose**: Controls access to the Application Load Balancer

- **Application Security Group** (EKS/ECS/EC2):
  - **Inbound Rules**: 
    - HTTP (80) from ALB security group
    - HTTPS (443) from ALB security group
  - **Outbound Rules**: 
    - HTTPS (443) to internet (0.0.0.0/0) for external API calls
    - TCP (5432) to RDS security group for database access
    - TCP (2049) to EFS security group for file system access
  - **Purpose**: Controls access to application components

- **RDS Security Group**:
  - **Inbound Rules**: 
    - PostgreSQL (5432) from application security group only
  - **Outbound Rules**: None (database does not initiate connections)
  - **Purpose**: Restricts database access to application components only

- **EFS Security Group**:
  - **Inbound Rules**: 
    - NFS (2049) from application security group only
  - **Outbound Rules**: None
  - **Purpose**: Restricts file system access to application components only

**Network ACLs (NACLs):**

- **Purpose**: Additional network-level security controls (stateless firewall)
- **Configuration**: 
  - Default NACLs allow all traffic (can be customized for stricter controls)
  - Custom NACLs can be created for subnet-level restrictions
- **Best Practice**: Use security groups for primary access control (stateful), NACLs for additional network-level restrictions if needed

**Route Tables:**

- **Public Route Table**:
  - **Routes**: 
    - 10.0.0.0/16 → Local (VPC internal)
    - 0.0.0.0/0 → Internet Gateway (public internet)
  - **Associated With**: Public subnets

- **Private Route Table**:
  - **Routes**: 
    - 10.0.0.0/16 → Local (VPC internal)
    - 0.0.0.0/0 → NAT Gateway (outbound internet)
  - **Associated With**: Private subnets

**NAT Gateway:**

- **Purpose**: Provides outbound internet access for resources in private subnets
- **Configuration**: 
  - Deployed in public subnet
  - Elastic IP address associated
  - Route table configured to route private subnet traffic to NAT Gateway
- **High Availability**: Deploy NAT Gateway in each availability zone for redundancy (recommended for production)

**VPC Endpoints (Optional):**

- **Purpose**: Private connectivity to AWS services without internet gateway or NAT Gateway
- **Services**: Can be configured for S3, Secrets Manager, CloudWatch Logs
- **Benefits**: Reduced data transfer costs, improved security, lower latency

### Instance Metadata Service (IMDS) Configuration

Corridor deployments support disabling Instance Metadata Service Version 1 (IMDSv1) to enhance security.

**IMDSv1 Disable Support:**

- **Requirement**: All components hosted in the customer's AWS account must support disabling IMDSv1
- **Compliance**: Corridor uses the latest AWS SDK versions, which automatically use IMDSv2 (Token-based authentication) when available

**Configuration:**

- **EKS Deployments**: 
  - EKS node groups can be configured to require IMDSv2
  - Set `metadata_options.http_tokens` to `required` in node group configuration
  - Application pods use IMDSv2 automatically via AWS SDK

- **ECS Fargate Deployments**: 
  - ECS tasks automatically use IMDSv2 when available
  - No additional configuration required

- **EC2 Deployments**: 
  - EC2 instances can be configured to require IMDSv2
  - Set `MetadataOptions.HttpTokens` to `required` during instance launch
  - Application code uses IMDSv2 automatically via AWS SDK

**Verification:**

```bash
# Verify IMDSv1 is disabled (should return 401 Unauthorized)
curl http://169.254.169.254/latest/meta-data/

# Verify IMDSv2 works (should return metadata)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/
```

**AWS SDK Compatibility:**

- Corridor uses AWS SDK versions that support IMDSv2 automatically
- SDKs automatically fall back to IMDSv2 when IMDSv1 is disabled
- No code changes required when disabling IMDSv1

## Typical Customer Deployment Overview

A typical Corridor deployment on AWS includes the following resources and components:

### Infrastructure Resources

- **Virtual Private Cloud (VPC)**: Isolated network environment with public and private subnets
- **Subnets**: Multiple availability zones for high availability (minimum 2 AZs for production)
- **NAT Gateway**: For outbound internet access from private subnets
- **Internet Gateway**: For public subnet internet access
- **Route Tables**: Network routing configuration
- **Security Groups**: Firewall rules for network access control
- **Network ACLs**: Additional network-level security controls

### Compute Resources

- **EKS Cluster** (Kubernetes option): Managed Kubernetes cluster with node groups
- **ECS Cluster** (Fargate option): Serverless container orchestration cluster
- **EC2 Instances** (VM option): Virtual machines running Corridor components
- **Application Load Balancer (ALB)**: HTTP(S) load balancing and SSL termination
- **Target Groups**: Backend service routing configuration

### Storage Resources

- **Amazon RDS PostgreSQL**: Managed database for metadata storage (Multi-AZ for production)
- **Amazon EFS**: Network file system for persistent storage (EKS/Fargate deployments)
- **Amazon S3**: Object storage for file management and backups
- **EBS Volumes**: Block storage for EC2 instances

### Application Components

- **corridor-app**: Web application server providing the analytical UI
- **corridor-api**: API server for business logic
- **corridor-worker-api**: Celery worker for asynchronous API tasks
- **corridor-worker-spark**: Celery worker for asynchronous Spark tasks
- **corridor-jupyter**: Jupyter Notebook server for analytical use
- **Redis**: Message queue for task orchestration

### Supporting Services

- **Route 53**: Domain name management and DNS configuration
- **AWS Secrets Manager**: Secure storage for sensitive configuration and credentials
- **CloudWatch**: Logging, monitoring, and alerting
- **AWS WAF**: Web application firewall for DDoS protection
- **CloudFront**: Content delivery network for static asset caching (optional)
- **cert-manager**: Automated TLS certificate management (EKS deployments)

### Post-Deployment Resources

- **IAM Roles and Policies**: Service roles for AWS resource access
- **Service Accounts**: Kubernetes service accounts (EKS deployments)
- **ConfigMaps and Secrets**: Kubernetes configuration management (EKS deployments)
- **Ingress Resources**: HTTP routing configuration (EKS deployments)

Upon completion of deployment, customers have a fully functional Corridor instance accessible via HTTPS with all components running, database initialized, and monitoring configured.

## Deployment Options

Corridor supports multiple deployment configurations on AWS to meet different availability and geographic requirements:

### Single-Availability Zone (Single-AZ)

A single-AZ deployment runs all resources within a single AWS Availability Zone. This configuration is suitable for:

- Development and testing environments
- Non-production workloads
- Cost-optimized deployments
- Scenarios where downtime tolerance is acceptable

**Characteristics:**
- Lower cost (no cross-AZ data transfer fees)
- Simpler network configuration
- Single point of failure for infrastructure components
- RDS can be configured as single-AZ (not recommended for production)

### Multi-Availability Zone (Multi-AZ)

A multi-AZ deployment distributes resources across multiple Availability Zones within a single AWS Region. This configuration provides:

- High availability and fault tolerance
- Automatic failover capabilities
- Production-ready resilience
- Data redundancy

**Characteristics:**
- RDS Multi-AZ deployment with automatic failover
- Application Load Balancer across multiple AZs
- EFS mount targets in each AZ
- EKS nodes distributed across AZs
- Higher cost due to cross-AZ data transfer

**Recommended for:** Production environments requiring high availability.

### Multi-Region

A multi-region deployment spans multiple AWS Regions for disaster recovery and geographic distribution. This configuration provides:

- Geographic redundancy and disaster recovery
- Reduced latency for global users
- Compliance with data residency requirements
- Cross-region failover capabilities

**Characteristics:**
- Primary and secondary region deployments
- Cross-region data replication
- Route 53 health checks and failover routing
- More complex networking and data synchronization
- Highest cost due to cross-region data transfer

**Recommended for:** Enterprise deployments requiring disaster recovery and global presence.

All three deployment options (EKS, ECS Fargate, and EC2) support single-AZ, multi-AZ, and multi-region configurations. The specific implementation details vary by deployment method and are documented in the respective installation guides.

## Expected Deployment Time

The expected time to complete a Corridor deployment on AWS is **30 minutes** for a standard single-AZ or multi-AZ deployment. This includes:

- Infrastructure provisioning (VPC, subnets, security groups)
- Database setup (RDS PostgreSQL)
- Storage configuration (EFS or S3)
- Application component deployment
- Initial configuration and verification

**Note:** Multi-region deployments may take longer (typically 45-60 minutes) due to additional networking and replication setup requirements.

Actual deployment time may vary based on:
- AWS service provisioning times
- Network configuration complexity
- Size of deployment (number of nodes/instances)
- Automation tooling used (Terraform, CloudFormation, etc.)

## Supported AWS Regions

Corridor can be deployed in all AWS Regions where the required services (EKS, ECS, EC2, RDS, EFS, S3) are available. Supported regions include:

### US Regions
- **US East (N. Virginia)** - `us-east-1`
- **US East (Ohio)** - `us-east-2`
- **US West (N. California)** - `us-west-1`
- **US West (Oregon)** - `us-west-2`

### Europe Regions
- **Europe (Ireland)** - `eu-west-1`
- **Europe (London)** - `eu-west-2`
- **Europe (Frankfurt)** - `eu-central-1`
- **Europe (Paris)** - `eu-west-3`
- **Europe (Stockholm)** - `eu-north-1`
- **Europe (Milan)** - `eu-south-1`

### Asia Pacific Regions
- **Asia Pacific (Tokyo)** - `ap-northeast-1`
- **Asia Pacific (Seoul)** - `ap-northeast-2`
- **Asia Pacific (Singapore)** - `ap-southeast-1`
- **Asia Pacific (Sydney)** - `ap-southeast-2`
- **Asia Pacific (Mumbai)** - `ap-south-1`
- **Asia Pacific (Hong Kong)** - `ap-east-1`

### Other Regions
- **Canada (Central)** - `ca-central-1`
- **South America (São Paulo)** - `sa-east-1`
- **Middle East (Bahrain)** - `me-south-1`
- **Middle East (UAE)** - `me-central-1`
- **Africa (Cape Town)** - `af-south-1`

**Note:** Some AWS services may have limited availability in certain regions. Verify service availability in your target region before deployment. For the most current list of supported regions and service availability, refer to the [AWS Regional Services List](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/).

## Cost and Licensing

This section provides information about AWS billable services, cost models, and licensing costs for Corridor deployments on AWS.

### Billable AWS Services

The following AWS services are used in Corridor deployments. Each service is categorized as mandatory or optional:

#### Mandatory Services

**Compute Services:**

- **Amazon EKS** (Kubernetes deployments) - **Mandatory**
  - **Cost Model**: Cluster management fee ($0.10/hour per cluster) + EC2 node costs
  - **Billing**: Hourly charges for cluster management and node instances
  - **Notes**: Required for EKS-based deployments

- **Amazon ECS Fargate** (Serverless deployments) - **Mandatory**
  - **Cost Model**: Pay-per-use based on vCPU and memory resources consumed
  - **Billing**: Charges for vCPU-hours and GB-hours of memory
  - **Notes**: Required for Fargate-based deployments

- **Amazon EC2** (VM deployments) - **Mandatory**
  - **Cost Model**: On-demand or reserved instance pricing based on instance type
  - **Billing**: Hourly charges for running instances
  - **Notes**: Required for EC2-based deployments

**Database Services:**

- **Amazon RDS PostgreSQL** - **Mandatory**
  - **Cost Model**: Instance pricing based on instance class, storage, and Multi-AZ configuration
  - **Billing**: Hourly charges for database instances + storage costs
  - **Notes**: Required for all deployment types. Multi-AZ adds ~2x cost for high availability

**Storage Services:**

- **Amazon EFS** (EKS/Fargate deployments) - **Mandatory**
  - **Cost Model**: Pay-per-use based on storage capacity (GB-month) + data transfer costs
  - **Billing**: Monthly charges for storage + data transfer fees
  - **Notes**: Required for EKS and Fargate deployments for persistent file storage

- **Amazon EBS** (EC2 deployments) - **Mandatory**
  - **Cost Model**: Volume pricing based on volume type and size (GB-month)
  - **Billing**: Monthly charges for provisioned storage
  - **Notes**: Required for EC2 deployments for local storage

- **Amazon S3** - **Mandatory**
  - **Cost Model**: Pay-per-use based on storage (GB-month), requests, and data transfer
  - **Billing**: Monthly charges for storage, PUT/GET requests, and data transfer
  - **Notes**: Required for backups and optional file storage

**Networking Services:**

- **Application Load Balancer (ALB)** - **Mandatory**
  - **Cost Model**: Hourly charges + data processing charges (per GB)
  - **Billing**: Hourly charges for load balancer + charges for data processed
  - **Notes**: Required for all deployments to provide HTTPS access

- **NAT Gateway** - **Mandatory**
  - **Cost Model**: Hourly charges + data processing charges (per GB)
  - **Billing**: Hourly charges + charges for data processed through NAT Gateway
  - **Notes**: Required for outbound internet access from private subnets

- **VPC** - **Mandatory** (No additional charge)
  - **Cost Model**: No additional charge for VPC itself
  - **Billing**: Included in AWS account (no separate charge)
  - **Notes**: Required for network isolation. Charges apply to resources within VPC

- **Data Transfer** - **Mandatory** (Usage-based)
  - **Cost Model**: Charges for data transfer out of AWS (per GB)
  - **Billing**: Charges for internet data transfer, cross-AZ transfer, cross-region transfer
  - **Notes**: Charges apply based on actual data transfer usage

#### Optional Services

**DNS and Domain Services:**

- **Amazon Route 53** - **Optional**
  - **Cost Model**: Hosted zone charges ($0.50/month) + query charges ($0.40 per million queries)
  - **Billing**: Monthly charges for hosted zones + per-query charges
  - **Notes**: Optional if using external DNS provider (e.g., Cloudflare, GoDaddy)

**Security and Compliance Services:**

- **AWS Secrets Manager** - **Optional**
  - **Cost Model**: $0.40 per secret per month + $0.05 per 10,000 API calls
  - **Billing**: Monthly charges per secret + API call charges
  - **Notes**: Optional but recommended for secure credential management. Can use environment variables or configuration files instead

- **AWS WAF** - **Optional**
  - **Cost Model**: $5 per web ACL per month + $1 per million requests
  - **Billing**: Monthly charges for web ACLs + per-request charges
  - **Notes**: Optional but recommended for production deployments for DDoS protection

**Monitoring and Logging Services:**

- **Amazon CloudWatch** - **Optional**
  - **Cost Model**: Free tier includes 10 custom metrics, 5 GB log ingestion, 10 GB log storage. Beyond free tier: $0.30 per custom metric, $0.50 per GB log ingestion, $0.03 per GB log storage
  - **Billing**: Charges for metrics, log ingestion, and log storage beyond free tier
  - **Notes**: Optional but recommended for production monitoring. Basic monitoring is included with EC2/EKS

- **CloudWatch Logs Insights** - **Optional**
  - **Cost Model**: $0.005 per GB of data scanned
  - **Billing**: Charges for log data scanned during queries
  - **Notes**: Optional for advanced log analysis

**Content Delivery:**

- **Amazon CloudFront** - **Optional**
  - **Cost Model**: Pay-per-use based on data transfer (per GB) and requests (per 10,000 requests)
  - **Billing**: Charges for data transfer out + request charges
  - **Notes**: Optional for static asset caching and CDN functionality

**Key Management:**

- **AWS KMS** - **Optional** (but recommended for encryption)
  - **Cost Model**: $1 per month per customer-managed key + $0.03 per 10,000 API requests
  - **Billing**: Monthly charges for keys + API request charges
  - **Notes**: Optional if using AWS-managed keys (free). Required for customer-managed encryption keys

**Certificate Management:**

- **AWS Certificate Manager (ACM)** - **Optional** (but recommended)
  - **Cost Model**: Free for public SSL/TLS certificates
  - **Billing**: No charge for public certificates
  - **Notes**: Optional if using Let's Encrypt (via cert-manager). Recommended for simplified certificate management

### Cost Model

Corridor deployments on AWS follow a pay-as-you-go cost model with the following cost components:

**Infrastructure Costs:**

- **Compute**: Costs vary by deployment method:
  - **EKS**: Cluster management fee + EC2 node costs (on-demand or reserved instances)
  - **ECS Fargate**: Pay-per-use based on vCPU and memory consumed
  - **EC2**: On-demand or reserved instance pricing based on instance type and size

- **Database**: RDS PostgreSQL instance costs based on:
  - Instance class (e.g., db.t3.medium, db.t3.xlarge)
  - Storage type and size (gp3, io1, io2)
  - Multi-AZ configuration (adds ~2x cost for high availability)
  - Backup storage (first 100% of provisioned storage is free)

- **Storage**: 
  - **EFS**: Pay-per-use based on storage capacity (Standard tier: ~$0.30/GB-month)
  - **EBS**: Provisioned storage costs (gp3: ~$0.08/GB-month)
  - **S3**: Tiered pricing based on storage class (Standard: ~$0.023/GB-month)

**Network Costs:**

- **Load Balancer**: Hourly charges (~$0.0225/hour) + data processing charges (~$0.008/GB)
- **NAT Gateway**: Hourly charges (~$0.045/hour) + data processing charges (~$0.045/GB)
- **Data Transfer**: 
  - Internet data transfer out: First 100 GB/month free, then ~$0.09/GB
  - Cross-AZ data transfer: ~$0.01/GB
  - Cross-region data transfer: ~$0.02/GB

**Operational Costs:**

- **Monitoring**: CloudWatch charges for metrics, logs, and alarms (free tier available)
- **Backup**: RDS backup storage costs (first 100% of provisioned storage free)
- **Secrets Management**: Secrets Manager charges if used (~$0.40/secret/month)

**Cost Optimization Recommendations:**

1. **Use Reserved Instances**: For predictable workloads, use EC2 or RDS Reserved Instances to save up to 75% compared to on-demand pricing
2. **Right-Size Resources**: Start with minimum required resources and scale based on actual usage
3. **Use Spot Instances**: For non-production environments, consider EC2 Spot Instances for EKS nodes (up to 90% savings)
4. **Optimize Storage**: Use appropriate storage classes (S3 Intelligent-Tiering, EFS Infrequent Access) for cost optimization
5. **Monitor Costs**: Set up AWS Cost Explorer and billing alerts to track and optimize spending
6. **Single-AZ for Development**: Use single-AZ deployments for development/testing to reduce costs
7. **Data Transfer Optimization**: Minimize cross-AZ and cross-region data transfer where possible

**Estimated Monthly Costs** (Example - Production Multi-AZ Deployment):

- **Small Deployment** (10-50 users):
  - Compute: $200-400/month
  - Database: $150-300/month
  - Storage: $50-100/month
  - Networking: $50-100/month
  - **Total**: ~$450-900/month

- **Medium Deployment** (50-200 users):
  - Compute: $400-800/month
  - Database: $300-600/month
  - Storage: $100-200/month
  - Networking: $100-200/month
  - **Total**: ~$900-1,800/month

- **Large Deployment** (200+ users):
  - Compute: $800-2,000/month
  - Database: $600-1,200/month
  - Storage: $200-500/month
  - Networking: $200-400/month
  - **Total**: ~$1,800-4,100/month

**Note:** Actual costs vary significantly based on:
- Deployment method (EKS vs ECS vs EC2)
- Instance sizes and types
- Data transfer volumes
- Storage requirements
- Multi-AZ vs single-AZ configuration
- Region selected
- Reserved Instance usage

Use the [AWS Pricing Calculator](https://calculator.aws/) for accurate cost estimates based on your specific requirements.

### Licensing Costs

**Corridor Software Licensing:**

- **License Model**: Corridor GenGuardX is licensed on a subscription basis
- **Pricing**: Contact Corridor sales for current licensing pricing and terms
- **License Components**: 
  - Base platform license (required)
  - Optional add-ons and premium features
  - Support and maintenance (included or optional tier)
- **License Scope**: License covers the Corridor software platform and does not include AWS infrastructure costs
- **Billing**: Licensing costs are separate from AWS infrastructure costs and billed directly by Corridor

**Third-Party Software Licensing:**

- **PostgreSQL**: Open-source (no license cost when using Amazon RDS)
- **Redis**: Open-source (no license cost)
- **Python**: Open-source (no license cost)
- **Java**: Open-source OpenJDK (no license cost)
- **Apache Spark**: Open-source (no license cost)
- **Kubernetes**: Open-source (no license cost when using Amazon EKS)

**AWS Service Licensing:**

- All AWS services are billed on a pay-as-you-go basis with no upfront licensing fees
- AWS services do not require separate software licenses
- Charges are based on actual usage of AWS resources

**Total Cost of Ownership (TCO):**

The total cost of running Corridor on AWS includes:
1. **Corridor Software License**: Subscription fee (contact sales for pricing)
2. **AWS Infrastructure Costs**: Pay-as-you-go charges for AWS services (see cost estimates above)
3. **Support Costs**: Included in license or optional support tiers
4. **Operational Costs**: Staff time for deployment, maintenance, and operations

**Note:** For accurate licensing pricing and terms, please contact Corridor sales or your account representative.

## Resource Sizing and Provisioning

This section provides guidance on selecting the appropriate type and size for AWS resources required for Corridor deployments. Automated provisioning scripts and Infrastructure-as-Code (IaC) templates are available in the detailed installation guides for each deployment method.

### Resource Provisioning Options

Corridor provides two approaches for provisioning AWS resources:

1. **Automated Provisioning Scripts**: Terraform and CloudFormation templates are available in the detailed installation guides ([EKS](./aws-eks.md), [ECS Fargate](./aws-fargate.md), [EC2](./aws-ec2.md)) that automate the creation of all required resources.

2. **Manual Provisioning Guidance**: Detailed guidance below for selecting resource types and sizes when provisioning manually or customizing automated scripts.

### Compute Resource Sizing

#### EKS Deployments

**EKS Cluster:**

- **Type**: Amazon EKS (Managed Kubernetes Service)
- **Sizing**: Single cluster per environment (development, staging, production)

**Node Groups:**

- **Development/Testing**: 
  - Instance Type: `m5.large` or `m5.xlarge`
  - Node Count: 2-3 nodes
  - Auto-scaling: Min 2, Max 5 nodes

- **Production (Small - 10-50 users)**:
  - Instance Type: `m5.xlarge` (4 vCPU, 16 GB RAM)
  - Node Count: 3 nodes (minimum for high availability)
  - Auto-scaling: Min 3, Max 8 nodes

- **Production (Medium - 50-200 users)**:
  - Instance Type: `m5.2xlarge` (8 vCPU, 32 GB RAM)
  - Node Count: 3-5 nodes
  - Auto-scaling: Min 3, Max 12 nodes

- **Production (Large - 200+ users)**:
  - Instance Type: `m5.4xlarge` (16 vCPU, 64 GB RAM) or `m5.8xlarge` (32 vCPU, 128 GB RAM)
  - Node Count: 5+ nodes
  - Auto-scaling: Min 5, Max 20 nodes

**Selection Criteria:**
- Start with `m5.xlarge` for production and scale based on actual usage
- Use `m5` instance family for general-purpose workloads
- Consider `c5` instances if CPU-intensive, `r5` if memory-intensive
- Distribute nodes across multiple availability zones for high availability

#### ECS Fargate Deployments

**ECS Cluster:**
- **Type**: Amazon ECS with Fargate launch type
- **Sizing**: Single cluster per environment

**Task Definitions (CPU and Memory):**
- **Development/Testing**:
  - **corridor-app**: 1 vCPU, 2 GB memory
  - **corridor-worker**: 1 vCPU, 2 GB memory
  - **corridor-jupyter**: 1 vCPU, 2 GB memory
  - **redis**: 0.5 vCPU, 1 GB memory
- **Production (Small - 10-50 users)**:
  - **corridor-app**: 2 vCPU, 4 GB memory
  - **corridor-worker**: 2 vCPU, 4 GB memory
  - **corridor-jupyter**: 2 vCPU, 4 GB memory
  - **redis**: 1 vCPU, 2 GB memory
- **Production (Medium - 50-200 users)**:
  - **corridor-app**: 4 vCPU, 8 GB memory
  - **corridor-worker**: 4 vCPU, 8 GB memory (scale horizontally)
  - **corridor-jupyter**: 4 vCPU, 8 GB memory
  - **redis**: 2 vCPU, 4 GB memory
- **Production (Large - 200+ users)**:
  - **corridor-app**: 4-8 vCPU, 8-16 GB memory
  - **corridor-worker**: 4-8 vCPU, 8-16 GB memory (scale horizontally)
  - **corridor-jupyter**: 4-8 vCPU, 8-16 GB memory
  - **redis**: 2-4 vCPU, 4-8 GB memory

**Selection Criteria:**
- Start with smaller sizes and use auto-scaling to scale based on demand
- Fargate automatically scales tasks based on CPU and memory utilization
- Monitor CloudWatch metrics to optimize task sizes

#### EC2 Deployments

**EC2 Instances:**
- **Development/Testing**:
  - Instance Type: `t3.xlarge` (4 vCPU, 16 GB RAM)
  - Instance Count: 1 instance
- **Production (Small - 10-50 users)**:
  - Instance Type: `t3.2xlarge` (8 vCPU, 32 GB RAM) - **Recommended minimum**
  - Instance Count: 1 instance (can add more for high availability)
- **Production (Medium - 50-200 users)**:
  - Instance Type: `m5.2xlarge` (8 vCPU, 32 GB RAM) or `m5.4xlarge` (16 vCPU, 64 GB RAM)
  - Instance Count: 1-2 instances
- **Production (Large - 200+ users)**:
  - Instance Type: `m5.4xlarge` (16 vCPU, 64 GB RAM) or `m5.8xlarge` (32 vCPU, 128 GB RAM)
  - Instance Count: 2+ instances (load balanced)

**Selection Criteria:**
- Use `t3` instances for burstable workloads (development, small production)
- Use `m5` instances for consistent performance requirements (medium/large production)
- Consider `c5` instances for CPU-intensive workloads, `r5` for memory-intensive workloads
- Ensure instance meets minimum requirements: 4 GB RAM, 4 CPU cores (see [Technical Prerequisites and Requirements](#technical-prerequisites-and-requirements))

### Database Resource Sizing

**Amazon RDS PostgreSQL:**

- **Development/Testing**:
  - Instance Class: `db.t3.medium` (2 vCPU, 4 GB RAM)
  - Storage: 20-50 GB (gp3)
  - Multi-AZ: Disabled (single-AZ)
- **Production (Small - 10-50 users)**:
  - Instance Class: `db.t3.xlarge` (4 vCPU, 16 GB RAM) - **Recommended minimum**
  - Storage: 100 GB (gp3)
  - Multi-AZ: Enabled (recommended)
- **Production (Medium - 50-200 users)**:
  - Instance Class: `db.m5.xlarge` (4 vCPU, 16 GB RAM) or `db.m5.2xlarge` (8 vCPU, 32 GB RAM)
  - Storage: 200-500 GB (gp3)
  - Multi-AZ: Enabled
- **Production (Large - 200+ users)**:
  - Instance Class: `db.m5.2xlarge` (8 vCPU, 32 GB RAM) or `db.m5.4xlarge` (16 vCPU, 64 GB RAM)
  - Storage: 500 GB - 1 TB (gp3 or io1/io2 for high IOPS)
  - Multi-AZ: Enabled

**Storage Type Selection:**
- **gp3**: General-purpose SSD (recommended for most workloads)
- **io1/io2**: Provisioned IOPS SSD (for high-performance database workloads requiring consistent IOPS)

**Selection Criteria:**
- Start with `db.t3.xlarge` for production and scale based on database performance metrics
- Monitor CloudWatch metrics (CPUUtilization, DatabaseConnections, ReadLatency, WriteLatency)
- Enable Multi-AZ for production environments for high availability
- Provisioned storage can be increased without downtime (storage autoscaling recommended)

### Storage Resource Sizing

#### Amazon EFS (EKS/Fargate Deployments)

- **Development/Testing**:
  - Storage: 50-100 GB
  - Performance Mode: General Purpose
  - Throughput Mode: Bursting
- **Production (Small - 10-50 users)**:
  - Storage: 100-500 GB
  - Performance Mode: General Purpose
  - Throughput Mode: Bursting or Provisioned (if consistent performance needed)
- **Production (Medium - 50-200 users)**:
  - Storage: 500 GB - 2 TB
  - Performance Mode: General Purpose
  - Throughput Mode: Provisioned (for consistent performance)
- **Production (Large - 200+ users)**:
  - Storage: 2 TB+
  - Performance Mode: General Purpose or Max I/O (for high concurrency)
  - Throughput Mode: Provisioned

**Selection Criteria:**
- EFS storage scales automatically (pay for what you use)
- Use General Purpose performance mode for most workloads
- Use Max I/O performance mode for applications with high levels of aggregate throughput and operations per second
- Enable lifecycle management to move infrequently accessed files to Infrequent Access (IA) storage class

#### Amazon EBS (EC2 Deployments)

- **Development/Testing**:
  - Volume Size: 50-100 GB
  - Volume Type: gp3
  - IOPS: 3,000 (gp3 baseline)
- **Production (Small - 10-50 users)**:
  - Volume Size: 100-200 GB
  - Volume Type: gp3
  - IOPS: 3,000-6,000
- **Production (Medium - 50-200 users)**:
  - Volume Size: 200-500 GB
  - Volume Type: gp3 or io1/io2
  - IOPS: 6,000-10,000
- **Production (Large - 200+ users)**:
  - Volume Size: 500 GB - 1 TB
  - Volume Type: gp3 or io1/io2
  - IOPS: 10,000+

**Selection Criteria:**
- Use gp3 for most workloads (cost-effective, good performance)
- Use io1/io2 for workloads requiring consistent IOPS (database workloads, high-transaction applications)
- Enable encryption at rest for all EBS volumes
- Monitor CloudWatch metrics (VolumeReadOps, VolumeWriteOps, VolumeQueueLength)

#### Amazon S3

- **Development/Testing**:
  - Storage: 10-50 GB
  - Storage Class: Standard
- **Production**:
  - Storage: Varies based on backup retention and file storage needs
  - Storage Class: Standard (frequently accessed), Intelligent-Tiering (unknown access patterns), Standard-IA (infrequently accessed)

**Selection Criteria:**
- Use Standard storage class for frequently accessed data
- Use Intelligent-Tiering for data with unknown or changing access patterns
- Use Standard-IA or Glacier for backups and archival data
- Enable lifecycle policies to automatically transition objects to appropriate storage classes

### Network Resource Sizing

#### Application Load Balancer (ALB)

- **Type**: Application Load Balancer
- **Sizing**: Single ALB per environment (can handle high traffic volumes)
- **Configuration**:
  - Scheme: Internet-facing
  - IP Address Type: IPv4
  - Subnets: Public subnets across multiple availability zones
  - Security Groups: Allow HTTPS (443) and HTTP (80) from internet

**Selection Criteria:**
- ALB automatically scales to handle traffic (no size selection needed)
- Deploy ALB in at least 2 availability zones for high availability
- Use AWS WAF in front of ALB for additional protection (optional)

#### NAT Gateway

- **Type**: NAT Gateway
- **Sizing**: One NAT Gateway per availability zone (for high availability)
- **Configuration**:
  - Elastic IP: Required (one per NAT Gateway)
  - Subnets: Public subnets

**Selection Criteria:**
- Deploy one NAT Gateway per availability zone for high availability (recommended for production)
- Single NAT Gateway is sufficient for development/testing environments
- NAT Gateway automatically scales (no size selection needed)

#### VPC and Subnets

- **VPC CIDR**: `/16` (e.g., 10.0.0.0/16) - provides 65,536 IP addresses
- **Public Subnets**: `/24` per availability zone (e.g., 10.0.1.0/24, 10.0.2.0/24) - 256 IP addresses each
- **Private Subnets**: `/24` per availability zone (e.g., 10.0.10.0/24, 10.0.11.0/24) - 256 IP addresses each

**Selection Criteria:**
- Use `/16` CIDR for VPC to allow for future growth
- Allocate `/24` subnets per availability zone (sufficient for most deployments)
- Ensure subnets don't overlap with existing network ranges

### Resource Sizing Summary Table

| Resource | Development | Small Production | Medium Production | Large Production |
|----------|-------------|------------------|------------------|-----------------|
| **EKS Nodes** | m5.large (2-3 nodes) | m5.xlarge (3 nodes) | m5.2xlarge (3-5 nodes) | m5.4xlarge+ (5+ nodes) |
| **ECS Tasks** | 1 vCPU, 2 GB | 2 vCPU, 4 GB | 4 vCPU, 8 GB | 4-8 vCPU, 8-16 GB |
| **EC2 Instance** | t3.xlarge | t3.2xlarge | m5.2xlarge | m5.4xlarge+ |
| **RDS Instance** | db.t3.medium | db.t3.xlarge | db.m5.xlarge | db.m5.2xlarge+ |
| **RDS Storage** | 20-50 GB | 100 GB | 200-500 GB | 500 GB - 1 TB |
| **EFS/EBS Storage** | 50-100 GB | 100-500 GB | 500 GB - 2 TB | 2 TB+ |

### Automated Provisioning Scripts

Terraform and CloudFormation templates are available in the detailed installation guides that automate the provisioning of all required resources with recommended sizing:

- **EKS Deployment**: See [EKS Installation Guide](./aws-eks.md) for Terraform templates and Kubernetes manifests
- **ECS Fargate Deployment**: See [Fargate Installation Guide](./aws-fargate.md) for CloudFormation templates and ECS task definitions
- **EC2 Deployment**: See [EC2 Installation Guide](./aws-ec2.md) for Terraform templates and AWS CLI scripts

These scripts include:
- Pre-configured resource sizes based on deployment type (development, production)
- Security best practices (encryption, security groups, IAM roles)
- High availability configurations (Multi-AZ, auto-scaling)
- Cost optimization settings

**Using Automated Scripts:**
1. Review the Terraform/CloudFormation templates in the respective installation guides
2. Customize variables (instance types, storage sizes) based on your requirements
3. Deploy using `terraform apply` or CloudFormation console/CLI
4. Monitor resource utilization and adjust sizes as needed

**Manual Provisioning:**
If provisioning manually, follow the sizing guidance above and refer to the [Technical Prerequisites and Requirements](#technical-prerequisites-and-requirements) section for minimum requirements.

### Monitoring and Right-Sizing

After deployment, monitor resource utilization using AWS CloudWatch and adjust sizes as needed:

- **CPU Utilization**: Target 40-70% average utilization
- **Memory Utilization**: Target 60-80% average utilization
- **Storage Utilization**: Monitor and scale before reaching 80% capacity
- **Network Throughput**: Monitor data transfer and optimize if needed

Use AWS Cost Explorer and CloudWatch metrics to identify opportunities for right-sizing and cost optimization.

## Step-by-Step Deployment Instructions

This section provides step-by-step instructions for deploying Corridor on AWS according to the typical deployment architecture described in the [Typical Customer Deployment Overview](#typical-customer-deployment-overview) section. The deployment follows a multi-AZ production architecture with high availability.

### Step 1: Provision Network Infrastructure

**1.1 Create VPC and Subnets**

```bash
# Create VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=corridor-vpc}]'

# Create public subnets (one per availability zone)
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.2.0/24 --availability-zone us-east-1b

# Create private subnets (one per availability zone)
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.10.0/24 --availability-zone us-east-1a
aws ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.11.0/24 --availability-zone us-east-1b
```

**1.2 Create Internet Gateway and NAT Gateway**

```bash
# Create and attach Internet Gateway
aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=corridor-igw}]'
aws ec2 attach-internet-gateway --internet-gateway-id <igw-id> --vpc-id <vpc-id>

# Allocate Elastic IP for NAT Gateway
aws ec2 allocate-address --domain vpc

# Create NAT Gateway in public subnet
aws ec2 create-nat-gateway --subnet-id <public-subnet-id> --allocation-id <eip-id>
```

**1.3 Configure Route Tables**

```bash
# Create route table for public subnets
aws ec2 create-route-table --vpc-id <vpc-id>
aws ec2 create-route --route-table-id <public-rt-id> --destination-cidr-block 0.0.0.0/0 --gateway-id <igw-id>

# Create route table for private subnets
aws ec2 create-route-table --vpc-id <vpc-id>
aws ec2 create-route --route-table-id <private-rt-id> --destination-cidr-block 0.0.0.0/0 --nat-gateway-id <nat-gw-id>
```

**1.4 Create Security Groups**

```bash
# Security group for Application Load Balancer
aws ec2 create-security-group --group-name corridor-alb-sg --description "Security group for ALB" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <alb-sg-id> --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id <alb-sg-id> --protocol tcp --port 80 --cidr 0.0.0.0/0

# Security group for application components
aws ec2 create-security-group --group-name corridor-app-sg --description "Security group for application" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> --protocol tcp --port 80 --source-group <alb-sg-id>
aws ec2 authorize-security-group-ingress --group-id <app-sg-id> --protocol tcp --port 443 --source-group <alb-sg-id>

# Security group for RDS database
aws ec2 create-security-group --group-name corridor-db-sg --description "Security group for RDS" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <db-sg-id> --protocol tcp --port 5432 --source-group <app-sg-id>

# Security group for EFS (if using EKS/Fargate)
aws ec2 create-security-group --group-name corridor-efs-sg --description "Security group for EFS" --vpc-id <vpc-id>
aws ec2 authorize-security-group-ingress --group-id <efs-sg-id> --protocol tcp --port 2049 --source-group <app-sg-id>
```

### Step 2: Provision Database Infrastructure

**2.1 Create DB Subnet Group**

```bash
aws rds create-db-subnet-group \
  --db-subnet-group-name corridor-db-subnet \
  --db-subnet-group-description "Subnet group for Corridor RDS" \
  --subnet-ids <private-subnet-1-id> <private-subnet-2-id>
```

**2.2 Create RDS PostgreSQL Instance**

```bash
aws rds create-db-instance \
  --db-instance-identifier corridor-db \
  --db-instance-class db.t3.xlarge \
  --engine postgres \
  --engine-version 14.9 \
  --master-username corridor \
  --master-user-password <secure-password> \
  --allocated-storage 100 \
  --storage-type gp3 \
  --storage-encrypted \
  --multi-az \
  --db-name corridor \
  --db-subnet-group-name corridor-db-subnet \
  --vpc-security-group-ids <db-sg-id> \
  --backup-retention-period 7 \
  --enable-cloudwatch-logs-export postgresql
```

**2.3 Store Database Credentials in Secrets Manager**

```bash
aws secretsmanager create-secret \
  --name corridor/database/credentials \
  --secret-string '{"username":"corridor","password":"<secure-password>","host":"<rds-endpoint>","port":"5432","database":"corridor"}'
```

### Step 3: Provision Storage Infrastructure

**For EKS/Fargate Deployments:**

**3.1 Create EFS File System**

```bash
# Create EFS file system
aws efs create-file-system \
  --creation-token corridor-efs \
  --performance-mode generalPurpose \
  --throughput-mode bursting \
  --encrypted

# Create mount targets in each private subnet
aws efs create-mount-target \
  --file-system-id <efs-id> \
  --subnet-id <private-subnet-1-id> \
  --security-groups <efs-sg-id>

aws efs create-mount-target \
  --file-system-id <efs-id> \
  --subnet-id <private-subnet-2-id> \
  --security-groups <efs-sg-id>
```

**For EC2 Deployments:**

**3.2 Create EBS Volume (if needed)**

```bash
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 100 \
  --volume-type gp3 \
  --encrypted
```

**3.3 Create S3 Bucket for Backups**

```bash
aws s3 mb s3://corridor-backups-<unique-id> --region us-east-1
aws s3api put-bucket-encryption \
  --bucket corridor-backups-<unique-id> \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

### Step 4: Provision Compute Infrastructure

**For EKS Deployment:**

**4.1 Create EKS Cluster**

```bash
# Create IAM role for EKS cluster
aws iam create-role --role-name corridor-eks-cluster-role \
  --assume-role-policy-document file://eks-cluster-trust-policy.json

# Attach required policies
aws iam attach-role-policy --role-name corridor-eks-cluster-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

# Create EKS cluster
aws eks create-cluster \
  --name corridor-cluster \
  --role-arn arn:aws:iam::<account-id>:role/corridor-eks-cluster-role \
  --resources-vpc-config subnetIds=<private-subnet-1-id>,<private-subnet-2-id>,endpointPrivateAccess=true,endpointPublicAccess=false \
  --version 1.28

# Create node group
aws eks create-nodegroup \
  --cluster-name corridor-cluster \
  --nodegroup-name corridor-nodes \
  --node-role arn:aws:iam::<account-id>:role/corridor-eks-node-role \
  --subnets <private-subnet-1-id> <private-subnet-2-id> \
  --instance-types m5.xlarge \
  --scaling-config minSize=3,maxSize=10,desiredSize=3
```

**For ECS Fargate Deployment:**

**4.2 Create ECS Cluster**

```bash
aws ecs create-cluster --cluster-name corridor-cluster --capacity-providers FARGATE FARGATE_SPOT
```

**For EC2 Deployment:**

**4.3 Launch EC2 Instance**

```bash
aws ec2 run-instances \
  --image-id ami-<latest-amazon-linux-2> \
  --instance-type t3.2xlarge \
  --subnet-id <private-subnet-id> \
  --security-group-ids <app-sg-id> \
  --iam-instance-profile Name=corridor-instance-profile \
  --user-data file://install-corridor.sh \
  --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":100,"VolumeType":"gp3","Encrypted":true}}]'
```

### Step 5: Create Application Load Balancer

**5.1 Create ALB**

```bash
aws elbv2 create-load-balancer \
  --name corridor-alb \
  --subnets <public-subnet-1-id> <public-subnet-2-id> \
  --security-groups <alb-sg-id> \
  --scheme internet-facing \
  --type application \
  --ip-address-type ipv4
```

**5.2 Create Target Group**

```bash
aws elbv2 create-target-group \
  --name corridor-targets \
  --protocol HTTP \
  --port 80 \
  --vpc-id <vpc-id> \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3
```

**5.3 Create Listener**

```bash
# Create HTTPS listener (requires SSL certificate)
aws elbv2 create-listener \
  --load-balancer-arn <alb-arn> \
  --protocol HTTPS \
  --port 443 \
  --certificates CertificateArn=<acm-certificate-arn> \
  --default-actions Type=forward,TargetGroupArn=<target-group-arn>

# Create HTTP listener (redirects to HTTPS)
aws elbv2 create-listener \
  --load-balancer-arn <alb-arn> \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=redirect,RedirectConfig='{Protocol=HTTPS,Port=443,StatusCode=HTTP_301}'
```

### Step 6: Deploy Corridor Application

**For EKS Deployment:**

**6.1 Install Cluster Components**

```bash
# Install AWS Load Balancer Controller
kubectl apply -f https://github.com/kubernetes-sigs/aws-load-balancer-controller/releases/download/v2.7.0/v2_7_0_full.yaml

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Install EFS CSI Driver
kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=release-1.7"
```

**6.2 Deploy Corridor**

```bash
# Create namespace
kubectl create namespace corridor

# Create secrets for database credentials
kubectl create secret generic corridor-db-credentials \
  --from-literal=username=corridor \
  --from-literal=password=<password> \
  --from-literal=host=<rds-endpoint> \
  --namespace corridor

# Apply Kubernetes manifests
kubectl apply -f corridor-manifests.yaml -n corridor
```

**For ECS Fargate Deployment:**

**6.3 Create Task Definition and Service**

```bash
# Register task definition
aws ecs register-task-definition --cli-input-json file://corridor-task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster corridor-cluster \
  --service-name corridor-service \
  --task-definition corridor-task \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<private-subnet-1-id>,<private-subnet-2-id>],securityGroups=[<app-sg-id>],assignPublicIp=DISABLED}" \
  --load-balancers targetGroupArn=<target-group-arn>,containerName=corridor-app,containerPort=80
```

**For EC2 Deployment:**

**6.4 Install Corridor Components**

```bash
# SSH into EC2 instance
ssh -i <key-pair>.pem ec2-user@<ec2-instance-ip>

# Install system dependencies
sudo yum update -y
sudo yum install -y python3.11 python3.11-devel java-1.8.0-openjdk redis nginx

# Extract and install Corridor bundle
cd /tmp
unzip corridor-bundle.zip
sudo ./corridor-bundle/install app -i /opt/corridor
sudo ./corridor-bundle/install api -i /opt/corridor
sudo ./corridor-bundle/install worker-api -i /opt/corridor
sudo ./corridor-bundle/install worker-spark -i /opt/corridor
sudo ./corridor-bundle/install jupyter -i /opt/corridor

# Configure database connection
sudo vi /opt/corridor/instances/default/config/api_config.py
# Update SQLALCHEMY_DATABASE_URI with RDS endpoint

# Initialize database
/opt/corridor/venv-api/bin/corridor-api db upgrade

# Start services
sudo systemctl start corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter
sudo systemctl enable corridor-app corridor-api corridor-worker-api corridor-worker-spark corridor-jupyter
```

### Step 7: Configure DNS and SSL

**7.1 Configure DNS**

```bash
# If using Route 53
aws route53 change-resource-record-sets \
  --hosted-zone-id <hosted-zone-id> \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "corridor.example.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "<alb-hosted-zone-id>",
          "DNSName": "<alb-dns-name>",
          "EvaluateTargetHealth": true
        }
      }
    }]
  }'

# If using external DNS provider, create A record pointing to ALB DNS name
```

**7.2 Verify SSL Certificate**

```bash
# For EKS with cert-manager, check certificate status
kubectl get certificate -n corridor

# For ACM certificates, verify in AWS Console or CLI
aws acm describe-certificate --certificate-arn <certificate-arn>
```

### Step 8: Post-Deployment Configuration

**8.1 Initialize Admin User**

```bash
# Access Corridor web interface via HTTPS
# Navigate to https://corridor.example.com
# Follow initial setup wizard to create admin user
```

**8.2 Configure Monitoring**

```bash
# Enable CloudWatch Container Insights (for EKS/ECS)
aws eks update-cluster-config --name corridor-cluster --logging '{"enable":[{"types":["api","audit","authenticator","controllerManager","scheduler"]}]}'

# Create CloudWatch alarms for key metrics
aws cloudwatch put-metric-alarm \
  --alarm-name corridor-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

**8.3 Verify Deployment**

```bash
# Check application health endpoint
curl https://corridor.example.com/health

# Verify all services are running
# For EKS: kubectl get pods -n corridor
# For ECS: aws ecs describe-services --cluster corridor-cluster --services corridor-service
# For EC2: sudo systemctl status corridor-app corridor-api
```

## Testing and Troubleshooting

This section provides prescriptive guidance for testing your Corridor deployment and troubleshooting common issues.

### Pre-Deployment Testing

Before deploying to production, test the deployment in a development or staging environment:

**1. Infrastructure Testing**

```bash
# Verify VPC connectivity
aws ec2 describe-vpcs --vpc-ids <vpc-id>

# Test security group rules
aws ec2 describe-security-groups --group-ids <sg-id>

# Verify NAT Gateway is working
# From an instance in private subnet, test internet connectivity
ping 8.8.8.8
```

**2. Database Connectivity Testing**

```bash
# Test RDS connectivity from application subnet
psql -h <rds-endpoint> -U corridor -d corridor

# Verify database credentials from Secrets Manager
aws secretsmanager get-secret-value --secret-id corridor/database/credentials
```

**3. Storage Testing**

```bash
# For EFS: Test mount from application instance
sudo mount -t efs <efs-id>:/ /mnt/efs
echo "test" > /mnt/efs/test.txt
cat /mnt/efs/test.txt

# For S3: Test bucket access
aws s3 ls s3://corridor-backups-<unique-id>/
aws s3 cp test.txt s3://corridor-backups-<unique-id>/
```

### Post-Deployment Testing

**1. Application Health Checks**

```bash
# Test health endpoint
curl https://corridor.example.com/health

# Expected response: {"status": "healthy", "version": "x.x.x"}

# Test API endpoint
curl https://corridor.example.com/api/v1/status

# Test web interface
curl -I https://corridor.example.com
```

**2. Component Testing**

**For EKS:**
```bash
# Check pod status
kubectl get pods -n corridor

# Check pod logs
kubectl logs -n corridor deploy/corridor-app --tail=100

# Test pod connectivity
kubectl exec -it -n corridor deploy/corridor-app -- curl http://localhost:8000/health
```

**For ECS:**
```bash
# Check task status
aws ecs describe-tasks --cluster corridor-cluster --tasks <task-id>

# Check task logs
aws logs tail /ecs/corridor --follow

# Test task connectivity
aws ecs execute-command --cluster corridor-cluster --task <task-id> --container corridor-app --command "/bin/sh"
```

**For EC2:**
```bash
# Check service status
sudo systemctl status corridor-app corridor-api corridor-worker-api

# Check service logs
sudo journalctl -u corridor-app -n 100
sudo tail -f /opt/corridor/logs/app.log

# Test service connectivity
curl http://localhost:8000/health
```

**3. Load Balancer Testing**

```bash
# Check ALB target health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>

# Test ALB routing
curl -H "Host: corridor.example.com" http://<alb-dns-name>/health

# Verify SSL certificate
openssl s_client -connect corridor.example.com:443 -servername corridor.example.com
```

**4. Database Testing**

```bash
# Test database connectivity from application
# Connect to application pod/instance and test database connection
python3 -c "import psycopg2; conn = psycopg2.connect(host='<rds-endpoint>', user='corridor', password='<password>', dbname='corridor'); print('Connected successfully')"

# Check database tables
psql -h <rds-endpoint> -U corridor -d corridor -c "\dt"
```

### Common Issues and Troubleshooting

**Issue 1: Application Not Accessible**

**Symptoms:** Cannot access application via HTTPS URL

**Troubleshooting Steps:**

1. **Verify DNS Configuration**
   ```bash
   # Check DNS resolution
   nslookup corridor.example.com
   dig corridor.example.com
   
   # Verify DNS points to ALB
   aws route53 list-resource-record-sets --hosted-zone-id <hosted-zone-id>
   ```

2. **Check Load Balancer Status**
   ```bash
   # Verify ALB is active
   aws elbv2 describe-load-balancers --load-balancer-arns <alb-arn>
   
   # Check target health
   aws elbv2 describe-target-health --target-group-arn <target-group-arn>
   ```

3. **Verify Security Groups**
   ```bash
   # Check ALB security group allows HTTPS
   aws ec2 describe-security-groups --group-ids <alb-sg-id>
   
   # Check application security group allows traffic from ALB
   aws ec2 describe-security-groups --group-ids <app-sg-id>
   ```

4. **Check SSL Certificate**
   ```bash
   # Verify certificate is valid
   aws acm describe-certificate --certificate-arn <cert-arn>
   
   # Test SSL connection
   openssl s_client -connect corridor.example.com:443
   ```

**Issue 2: Database Connection Failures**

**Symptoms:** Application cannot connect to RDS database

**Troubleshooting Steps:**

1. **Verify Database Endpoint**
   ```bash
   # Check RDS instance status
   aws rds describe-db-instances --db-instance-identifier corridor-db
   
   # Verify endpoint is correct
   aws rds describe-db-instances --db-instance-identifier corridor-db --query 'DBInstances[0].Endpoint.Address'
   ```

2. **Check Security Groups**
   ```bash
   # Verify RDS security group allows PostgreSQL from application
   aws ec2 describe-security-groups --group-ids <db-sg-id>
   
   # Test connectivity from application subnet
   telnet <rds-endpoint> 5432
   ```

3. **Verify Credentials**
   ```bash
   # Check credentials in Secrets Manager
   aws secretsmanager get-secret-value --secret-id corridor/database/credentials
   
   # Test connection with credentials
   psql -h <rds-endpoint> -U corridor -d corridor
   ```

4. **Check Database Status**
   ```bash
   # Verify database is available
   aws rds describe-db-instances --db-instance-identifier corridor-db --query 'DBInstances[0].DBInstanceStatus'
   ```

**Issue 3: Pod/Container Failures (EKS/ECS)**

**Symptoms:** Pods or containers are crashing or not starting

**Troubleshooting Steps:**

**For EKS:**
```bash
# Check pod status
kubectl get pods -n corridor

# Describe pod for events
kubectl describe pod <pod-name> -n corridor

# Check pod logs
kubectl logs <pod-name> -n corridor --previous

# Check resource limits
kubectl top pod <pod-name> -n corridor
```

**For ECS:**
```bash
# Check task status
aws ecs describe-tasks --cluster corridor-cluster --tasks <task-id>

# Check task logs
aws logs tail /ecs/corridor --follow

# Check task definition
aws ecs describe-task-definition --task-definition corridor-task
```

**Issue 4: Storage Mount Failures**

**Symptoms:** EFS or EBS volumes not mounting correctly

**Troubleshooting Steps:**

1. **For EFS:**
   ```bash
   # Verify EFS file system exists
   aws efs describe-file-systems --file-system-id <efs-id>
   
   # Check mount targets
   aws efs describe-mount-targets --file-system-id <efs-id>
   
   # Test mount from application instance
   sudo mount -t efs -o tls <efs-id>:/ /mnt/efs
   ```

2. **For EBS:**
   ```bash
   # Verify volume is attached
   aws ec2 describe-volumes --volume-ids <volume-id>
   
   # Check volume attachment
   aws ec2 describe-instances --instance-ids <instance-id> --query 'Instances[0].BlockDeviceMappings'
   ```

**Issue 5: High CPU or Memory Usage**

**Symptoms:** Application performance degradation, timeouts

**Troubleshooting Steps:**

1. **Monitor Resource Usage**
   ```bash
   # For EKS
   kubectl top nodes
   kubectl top pods -n corridor
   
   # For ECS
   aws cloudwatch get-metric-statistics \
     --namespace AWS/ECS \
     --metric-name CPUUtilization \
     --dimensions Name=ServiceName,Value=corridor-service \
     --start-time <start-time> \
     --end-time <end-time> \
     --period 300 \
     --statistics Average
   ```

2. **Check Application Logs**
   ```bash
   # Look for errors or warnings
   kubectl logs -n corridor deploy/corridor-app --tail=500 | grep -i error
   ```

3. **Scale Resources**
   ```bash
   # For EKS: Scale node group
   aws eks update-nodegroup-config --cluster-name corridor-cluster --nodegroup-name corridor-nodes --scaling-config minSize=5,maxSize=15
   
   # For ECS: Update service desired count
   aws ecs update-service --cluster corridor-cluster --service corridor-service --desired-count 4
   ```

### Getting Additional Help

If you encounter issues not covered in this guide:

1. **Check Application Logs**: Review application logs for error messages
2. **Review AWS CloudWatch**: Check CloudWatch metrics and logs for infrastructure issues
3. **Contact Corridor Support**: Reach out to Corridor support with:
   - Deployment method (EKS/ECS/EC2)
   - Error messages and logs
   - Steps to reproduce the issue
   - AWS region and resource IDs
4. **AWS Support**: For AWS infrastructure issues, contact AWS Support

## Health Monitoring and Assessment

This section provides step-by-step instructions for assessing and monitoring the health and proper function of the Corridor application deployed on AWS. Regular health monitoring ensures the application is operating correctly and helps identify issues before they impact users.

### Step 1: Configure Application Health Checks

**1.1 Application Health Endpoint**

The Corridor application exposes a health endpoint at `/health` that returns the application status:

```bash
# Test health endpoint
curl https://corridor.example.com/health

# Expected response:
# {"status": "healthy", "version": "x.x.x", "timestamp": "2024-01-01T00:00:00Z"}
```

**1.2 Configure Load Balancer Health Checks**

**For Application Load Balancer:**

```bash
# Update target group health check settings
aws elbv2 modify-target-group \
  --target-group-arn <target-group-arn> \
  --health-check-path /health \
  --health-check-interval-seconds 30 \
  --health-check-timeout-seconds 5 \
  --healthy-threshold-count 2 \
  --unhealthy-threshold-count 3 \
  --health-check-protocol HTTP \
  --health-check-port 80

# Verify health check configuration
aws elbv2 describe-target-groups --target-group-arns <target-group-arn>
```

**For EKS Deployments:**

```yaml
# Add health check to Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: corridor-app
spec:
  template:
    spec:
      containers:
      - name: corridor-app
        livenessProbe:
          httpGet:
            path: /health
            port: 5002
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 5002
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
```

**For ECS Deployments:**

```json
{
  "healthCheck": {
    "command": ["CMD-SHELL", "curl -f http://localhost:5002/health || exit 1"],
    "interval": 30,
    "timeout": 5,
    "retries": 3,
    "startPeriod": 60
  }
}
```

**1.3 Verify Health Check Status**

```bash
# Check target health status
aws elbv2 describe-target-health --target-group-arn <target-group-arn>

# Expected output shows "healthy" status for all targets
```

### Step 2: Set Up CloudWatch Metrics and Alarms

**2.1 Enable CloudWatch Container Insights (EKS/ECS)**

**For EKS:**

```bash
# Enable Container Insights
aws eks update-cluster-config \
  --name corridor-cluster \
  --logging '{
    "enable": [
      {"types": ["api", "audit", "authenticator", "controllerManager", "scheduler"]}
    ]
  }'

# Install CloudWatch Container Insights
kubectl apply -f https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml
```

**For ECS:**

```bash
# Container Insights is automatically enabled for ECS Fargate
# Verify in ECS console: Cluster → Monitoring → Container Insights
```

**2.2 Create CloudWatch Alarms for Application Health**

**Alarm 1: Application Health Check Failures**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name corridor-health-check-failures \
  --alarm-description "Alert when application health checks fail" \
  --metric-name HealthyHostCount \
  --namespace AWS/ApplicationELB \
  --statistic Minimum \
  --period 60 \
  --threshold 1 \
  --comparison-operator LessThanThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:sns:us-east-1:<account-id>:corridor-alerts
```

**Alarm 2: High CPU Utilization**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name corridor-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=ServiceName,Value=corridor-service Name=ClusterName,Value=corridor-cluster
```

**Alarm 3: High Memory Utilization**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name corridor-high-memory \
  --alarm-description "Alert when memory exceeds 85%" \
  --metric-name MemoryUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 85 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=ServiceName,Value=corridor-service Name=ClusterName,Value=corridor-cluster
```

**Alarm 4: Database Connection Errors**

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name corridor-db-connection-errors \
  --alarm-description "Alert on database connection errors" \
  --metric-name DatabaseConnections \
  --namespace AWS/RDS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 1 \
  --dimensions Name=DBInstanceIdentifier,Value=corridor-db
```

**2.3 Create SNS Topic for Alarms**

```bash
# Create SNS topic for alerts
aws sns create-topic --name corridor-alerts

# Subscribe email to topic
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:<account-id>:corridor-alerts \
  --protocol email \
  --notification-endpoint admin@example.com
```

### Step 3: Monitor Application Logs

**3.1 Configure Log Aggregation**

**For EKS:**

```bash
# Verify Fluentd/CloudWatch Logs integration
kubectl get daemonset -n amazon-cloudwatch

# Check log streams
aws logs describe-log-streams --log-group-name /aws/eks/corridor-cluster/cluster
```

**For ECS:**

```bash
# Logs are automatically sent to CloudWatch Logs
# Check log groups
aws logs describe-log-groups --log-group-name-prefix /ecs/corridor
```

**For EC2:**

```bash
# Install CloudWatch Agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
sudo rpm -U ./amazon-cloudwatch-agent.rpm

# Configure CloudWatch Agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

**3.2 Monitor Application Logs**

```bash
# View recent application logs
aws logs tail /ecs/corridor --follow

# Filter for errors
aws logs filter-log-events \
  --log-group-name /ecs/corridor \
  --filter-pattern "ERROR" \
  --start-time $(date -d '1 hour ago' +%s)000

# Search for specific patterns
aws logs filter-log-events \
  --log-group-name /ecs/corridor \
  --filter-pattern "database connection" \
  --start-time $(date -d '24 hours ago' +%s)000
```

### Step 4: Monitor Database Health

**4.1 Check RDS Instance Status**

```bash
# Check database instance status
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].[DBInstanceStatus,DBInstanceClass,MultiAZ,BackupRetentionPeriod]'

# Expected output:
# - DBInstanceStatus: "available"
# - MultiAZ: true (for production)
# - BackupRetentionPeriod: 7 (or higher)
```

**4.2 Monitor Database Metrics**

```bash
# Check database CPU utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name CPUUtilization \
  --dimensions Name=DBInstanceIdentifier,Value=corridor-db \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average

# Check database connections
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name DatabaseConnections \
  --dimensions Name=DBInstanceIdentifier,Value=corridor-db \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum
```

**4.3 Test Database Connectivity**

```bash
# Test database connection from application
# For EKS:
kubectl exec -it -n corridor deploy/corridor-app -- \
  python3 -c "import psycopg2; conn = psycopg2.connect(host='<rds-endpoint>', user='corridor', password='<password>', dbname='corridor'); print('Connected successfully')"

# For ECS:
aws ecs execute-command \
  --cluster corridor-cluster \
  --task <task-id> \
  --container corridor-app \
  --command "python3 -c \"import psycopg2; conn = psycopg2.connect(host='<rds-endpoint>', user='corridor', password='<password>', dbname='corridor'); print('Connected successfully')\""

# For EC2:
psql -h <rds-endpoint> -U corridor -d corridor -c "SELECT version();"
```

**4.4 Check Database Backup Status**

```bash
# List recent backups
aws rds describe-db-snapshots \
  --db-instance-identifier corridor-db \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,Status,SnapshotCreateTime]' \
  --output table

# Verify automated backups are enabled
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].[BackupRetentionPeriod,AutomatedBackups]'
```

### Step 5: Monitor Storage Health

**5.1 Monitor EFS File System (EKS/Fargate)**

```bash
# Check EFS file system status
aws efs describe-file-systems --file-system-id <efs-id>

# Check mount target status
aws efs describe-mount-targets --file-system-id <efs-id>

# Monitor EFS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EFS \
  --metric-name StorageBytes \
  --dimensions Name=FileSystemId,Value=<efs-id> \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average
```

**5.2 Monitor EBS Volumes (EC2)**

```bash
# Check EBS volume status
aws ec2 describe-volumes \
  --volume-ids <volume-id> \
  --query 'Volumes[0].[State,Size,VolumeType,Iops]'

# Monitor EBS metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/EBS \
  --metric-name VolumeReadOps \
  --dimensions Name=VolumeId,Value=<volume-id> \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

**5.3 Monitor S3 Bucket Health**

```bash
# Check S3 bucket metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value=corridor-backups Name=StorageType,Value=StandardStorage \
  --start-time $(date -u -d '1 day ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 3600 \
  --statistics Average
```

### Step 6: Monitor Network Health

**6.1 Monitor Load Balancer Health**

```bash
# Check target health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>

# Monitor ALB metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name TargetResponseTime \
  --dimensions Name=LoadBalancer,Value=<alb-arn-suffix> \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average

# Check HTTP error rates
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApplicationELB \
  --metric-name HTTPCode_Target_5XX_Count \
  --dimensions Name=LoadBalancer,Value=<alb-arn-suffix> \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

**6.2 Monitor NAT Gateway Health**

```bash
# Check NAT Gateway status
aws ec2 describe-nat-gateways --nat-gateway-ids <nat-gateway-id>

# Monitor NAT Gateway metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/NATGateway \
  --metric-name BytesOutToDestination \
  --dimensions Name=NatGatewayId,Value=<nat-gateway-id> \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

### Step 7: Perform Regular Health Assessments

**7.1 Daily Health Check Routine**

Perform these checks daily:

```bash
# 1. Check application health endpoint
curl https://corridor.example.com/health

# 2. Verify all targets are healthy
aws elbv2 describe-target-health --target-group-arn <target-group-arn> | grep -c "healthy"

# 3. Check for recent errors in logs
aws logs filter-log-events \
  --log-group-name /ecs/corridor \
  --filter-pattern "ERROR" \
  --start-time $(date -d '24 hours ago' +%s)000

# 4. Verify database is available
aws rds describe-db-instances --db-instance-identifier corridor-db --query 'DBInstances[0].DBInstanceStatus'

# 5. Check CloudWatch alarms
aws cloudwatch describe-alarms --alarm-names corridor-health-check-failures corridor-high-cpu corridor-high-memory
```

**7.2 Weekly Health Assessment**

Perform these checks weekly:

```bash
# 1. Review CloudWatch metrics trends
# Check CPU and memory trends over the past week
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=corridor-service \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 3600 \
  --statistics Average,Maximum

# 2. Review database performance
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name ReadLatency \
  --dimensions Name=DBInstanceIdentifier,Value=corridor-db \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 3600 \
  --statistics Average,Maximum

# 3. Verify backup completion
aws rds describe-db-snapshots \
  --db-instance-identifier corridor-db \
  --snapshot-type automated \
  --query 'DBSnapshots[0].[DBSnapshotIdentifier,SnapshotCreateTime]'

# 4. Review storage usage trends
aws cloudwatch get-metric-statistics \
  --namespace AWS/EFS \
  --metric-name StorageBytes \
  --dimensions Name=FileSystemId,Value=<efs-id> \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 3600 \
  --statistics Average,Maximum
```

**7.3 Monthly Health Review**

Perform these checks monthly:

```bash
# 1. Review cost trends
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d '1 month ago' +%Y-%m-01),End=$(date -u +%Y-%m-01) \
  --granularity MONTHLY \
  --metrics BlendedCost

# 2. Review security group rules
aws ec2 describe-security-groups --group-ids <sg-id>

# 3. Review IAM access patterns
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AssumeRole \
  --start-time $(date -u -d '1 month ago' +%Y-%m-%dT%H:%M:%S) \
  --max-results 100

# 4. Review application performance trends
# Compare response times, error rates, and resource utilization
```

### Step 8: Create Health Monitoring Dashboard

**8.1 Create CloudWatch Dashboard**

```bash
# Create dashboard JSON configuration
cat > dashboard.json <<EOF
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ApplicationELB", "HealthyHostCount", {"stat": "Average", "label": "Healthy Targets"}],
          [".", "UnHealthyHostCount", {"stat": "Average", "label": "Unhealthy Targets"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Load Balancer Health"
      }
    },
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/ECS", "CPUUtilization", {"stat": "Average", "label": "CPU"}],
          [".", "MemoryUtilization", {"stat": "Average", "label": "Memory"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Application Resources"
      }
    },
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/RDS", "CPUUtilization", {"stat": "Average", "label": "CPU"}],
          [".", "DatabaseConnections", {"stat": "Average", "label": "Connections"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "Database Health"
      }
    }
  ]
}
EOF

# Create dashboard
aws cloudwatch put-dashboard \
  --dashboard-name CorridorHealthDashboard \
  --dashboard-body file://dashboard.json
```

**8.2 Access Dashboard**

```bash
# View dashboard URL
echo "https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=CorridorHealthDashboard"
```

## Backup and Recovery

This section identifies the data stores and configurations that need to be backed up, and provides step-by-step instructions for backup and recovery procedures.

### Data Stores and Configurations for Backup

The following data stores and configurations must be backed up to ensure complete recovery capability:

**1. Metadata Database (Amazon RDS PostgreSQL)**

- **Data Type**: Application metadata, user accounts, pipelines, prompts, models, RAG configurations, evaluation results, audit logs
- **Backup Method**: RDS automated backups and manual snapshots
- **Backup Frequency**: 
  - Automated backups: Daily (retention period: 7-35 days)
  - Manual snapshots: Before major changes or weekly
- **Storage Location**: RDS backup storage (automated) or S3 (manual snapshots)

**2. File Storage**

- **EKS/Fargate Deployments**: Amazon EFS file system
  - **Data Type**: Uploaded files, datasets, generated artifacts, temporary files
  - **Backup Method**: EFS-to-EFS backup or EFS-to-S3 backup
  - **Backup Frequency**: Daily incremental, weekly full
- **EC2 Deployments**: EBS volumes or local filesystem
  - **Data Type**: Uploaded files, datasets, generated artifacts
  - **Backup Method**: EBS snapshots or file system backups
  - **Backup Frequency**: Daily snapshots

**3. Application Configuration**

- **Data Type**: Configuration files, environment variables, secrets
- **Backup Method**: Version control (Git) or S3 backups
- **Backup Frequency**: Before configuration changes
- **Location**: 
  - Kubernetes ConfigMaps/Secrets (EKS)
  - ECS task definitions (ECS)
  - Configuration files on EC2 instances

**4. SSL/TLS Certificates**

- **Data Type**: SSL certificates and private keys
- **Backup Method**: Export certificates from ACM or cert-manager
- **Backup Frequency**: Before certificate renewal
- **Storage Location**: Secure S3 bucket or secure file storage

**5. IAM Roles and Policies**

- **Data Type**: IAM role definitions, policies, trust relationships
- **Backup Method**: Infrastructure-as-Code (Terraform/CloudFormation) or AWS CLI export
- **Backup Frequency**: Before IAM changes
- **Storage Location**: Version control or S3

### Step-by-Step Backup Procedures

#### Database Backup

**Automated RDS Backups:**

```bash
# Verify automated backups are enabled
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].[BackupRetentionPeriod,AutomatedBackups]'

# List recent automated backups
aws rds describe-db-snapshots \
  --db-instance-identifier corridor-db \
  --snapshot-type automated \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,SnapshotCreateTime,Status]' \
  --output table
```

**Manual Database Snapshot:**

```bash
# Create manual snapshot
aws rds create-db-snapshot \
  --db-snapshot-identifier corridor-db-manual-$(date +%Y%m%d-%H%M%S) \
  --db-instance-identifier corridor-db

# Wait for snapshot completion
aws rds wait db-snapshot-completed \
  --db-snapshot-identifier corridor-db-manual-$(date +%Y%m%d-%H%M%S)

# Copy snapshot to another region (for disaster recovery)
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier corridor-db-manual-$(date +%Y%m%d-%H%M%S) \
  --target-db-snapshot-identifier corridor-db-backup-$(date +%Y%m%d-%H%M%S) \
  --target-region us-west-2
```

**Proprietary Database Export (Corridor API):**

```bash
# For EKS deployments
kubectl exec -it -n corridor deploy/corridor-api -- \
  /opt/corridor/venv-api/bin/corridor-api db export \
  --output /tmp/corridor-backup-$(date +%Y%m%d).sqlite

# Copy export file to S3
kubectl cp corridor/<pod-name>:/tmp/corridor-backup-$(date +%Y%m%d).sqlite \
  ./corridor-backup-$(date +%Y%m%d).sqlite

aws s3 cp corridor-backup-$(date +%Y%m%d).sqlite \
  s3://corridor-backups-<unique-id>/database/

# For EC2 deployments
/opt/corridor/venv-api/bin/corridor-api db export \
  --output /opt/corridor/backups/corridor-backup-$(date +%Y%m%d).sqlite

aws s3 cp /opt/corridor/backups/corridor-backup-$(date +%Y%m%d).sqlite \
  s3://corridor-backups-<unique-id>/database/
```

#### File Storage Backup

**EFS Backup (EKS/Fargate):**

```bash
# Create EFS backup using AWS Backup
aws backup create-backup-vault --backup-vault-name corridor-efs-backup-vault

aws backup start-backup-job \
  --backup-vault-name corridor-efs-backup-vault \
  --resource-arn arn:aws:elasticfilesystem:us-east-1:<account-id>:file-system/<efs-id> \
  --iam-role-arn arn:aws:iam::<account-id>:role/service-role/AWSBackupDefaultServiceRole

# Or use DataSync to copy to S3
aws datasync create-location-efs \
  --efs-filesystem-arn arn:aws:elasticfilesystem:us-east-1:<account-id>:file-system/<efs-id> \
  --ec2-config SubnetArn=arn:aws:ec2:us-east-1:<account-id>:subnet/<subnet-id>,SecurityGroupArns=arn:aws:ec2:us-east-1:<account-id>:security-group/<sg-id>

aws datasync create-location-s3 \
  --s3-bucket-arn arn:aws:s3:::corridor-backups-<unique-id> \
  --s3-config BucketAccessRoleArn=arn:aws:iam::<account-id>:role/DataSyncS3Role

aws datasync create-task \
  --source-location-arn <efs-location-arn> \
  --destination-location-arn <s3-location-arn> \
  --name corridor-efs-backup-task
```

**EBS Snapshot Backup (EC2):**

```bash
# Create EBS snapshot
aws ec2 create-snapshot \
  --volume-id <volume-id> \
  --description "Corridor EBS backup $(date +%Y%m%d-%H%M%S)" \
  --tag-specifications 'ResourceType=snapshot,Tags=[{Key=Name,Value=corridor-ebs-backup}]'

# Copy snapshot to another region
aws ec2 copy-snapshot \
  --source-region us-east-1 \
  --source-snapshot-id <snapshot-id> \
  --region us-west-2 \
  --description "Corridor EBS backup copy"
```

#### Configuration Backup

**Kubernetes ConfigMaps and Secrets (EKS):**

```bash
# Backup all ConfigMaps
kubectl get configmaps -n corridor -o yaml > corridor-configmaps-backup-$(date +%Y%m%d).yaml

# Backup all Secrets (without sensitive data in output)
kubectl get secrets -n corridor -o yaml > corridor-secrets-backup-$(date +%Y%m%d).yaml

# Upload to S3
aws s3 cp corridor-configmaps-backup-$(date +%Y%m%d).yaml \
  s3://corridor-backups-<unique-id>/config/
aws s3 cp corridor-secrets-backup-$(date +%Y%m%d).yaml \
  s3://corridor-backups-<unique-id>/config/
```

**ECS Task Definitions:**

```bash
# Export task definition
aws ecs describe-task-definition \
  --task-definition corridor-task \
  --query 'taskDefinition' > corridor-task-definition-backup-$(date +%Y%m%d).json

aws s3 cp corridor-task-definition-backup-$(date +%Y%m%d).json \
  s3://corridor-backups-<unique-id>/config/
```

**EC2 Configuration Files:**

```bash
# Backup configuration directory
tar -czf corridor-config-backup-$(date +%Y%m%d).tar.gz \
  /opt/corridor/instances/default/config

aws s3 cp corridor-config-backup-$(date +%Y%m%d).tar.gz \
  s3://corridor-backups-<unique-id>/config/
```

### Step-by-Step Recovery Procedures

#### Database Recovery

**Restore from RDS Snapshot:**

```bash
# List available snapshots
aws rds describe-db-snapshots \
  --db-instance-identifier corridor-db \
  --query 'DBSnapshots[*].[DBSnapshotIdentifier,SnapshotCreateTime]' \
  --output table

# Restore database from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier corridor-db-restored \
  --db-snapshot-identifier corridor-db-manual-20240101-120000 \
  --db-instance-class db.t3.xlarge

# Update application configuration to point to restored database
# For EKS: Update ConfigMap/Secret with new database endpoint
# For ECS: Update task definition with new database endpoint
# For EC2: Update configuration file with new database endpoint
```

**Restore from Proprietary Export:**

```bash
# Download export file from S3
aws s3 cp s3://corridor-backups-<unique-id>/database/corridor-backup-20240101.sqlite \
  ./corridor-backup-20240101.sqlite

# Import into database
# For EKS:
kubectl cp ./corridor-backup-20240101.sqlite \
  corridor/<pod-name>:/tmp/corridor-backup-20240101.sqlite

kubectl exec -it -n corridor deploy/corridor-api -- \
  /opt/corridor/venv-api/bin/corridor-api db import \
  --input /tmp/corridor-backup-20240101.sqlite

# For EC2:
/opt/corridor/venv-api/bin/corridor-api db import \
  --input ./corridor-backup-20240101.sqlite
```

#### File Storage Recovery

**Restore EFS from Backup:**

```bash
# Restore from AWS Backup
aws backup start-restore-job \
  --recovery-point-arn <recovery-point-arn> \
  --iam-role-arn arn:aws:iam::<account-id>:role/service-role/AWSBackupDefaultServiceRole \
  --resource-type EFS \
  --metadata file-system-id=<efs-id>,new-file-system=true

# Or restore from S3 using DataSync
aws datasync start-task-execution --task-arn <task-arn>
```

**Restore EBS from Snapshot:**

```bash
# Create volume from snapshot
aws ec2 create-volume \
  --snapshot-id <snapshot-id> \
  --availability-zone us-east-1a \
  --volume-type gp3

# Attach volume to instance
aws ec2 attach-volume \
  --volume-id <volume-id> \
  --instance-id <instance-id> \
  --device /dev/xvdf

# Mount volume on instance
sudo mount /dev/xvdf /mnt/restored-data
```

#### Configuration Recovery

**Restore Kubernetes ConfigMaps/Secrets:**

```bash
# Download from S3
aws s3 cp s3://corridor-backups-<unique-id>/config/corridor-configmaps-backup-20240101.yaml \
  ./corridor-configmaps-backup-20240101.yaml

# Apply restored ConfigMaps
kubectl apply -f corridor-configmaps-backup-20240101.yaml -n corridor

# Restart pods to pick up new configuration
kubectl rollout restart deployment -n corridor
```

**Restore ECS Task Definition:**

```bash
# Download from S3
aws s3 cp s3://corridor-backups-<unique-id>/config/corridor-task-definition-backup-20240101.json \
  ./corridor-task-definition-backup-20240101.json

# Register restored task definition
aws ecs register-task-definition \
  --cli-input-json file://corridor-task-definition-backup-20240101.json

# Update service to use restored task definition
aws ecs update-service \
  --cluster corridor-cluster \
  --service corridor-service \
  --task-definition corridor-task
```

### Automated Backup Schedule

**Recommended Backup Schedule:**

- **Database**: 
  - Automated backups: Daily (retention: 7-35 days)
  - Manual snapshots: Weekly or before major changes
  - Cross-region copies: Monthly
- **File Storage**: 
  - EFS: Daily incremental, weekly full
  - EBS: Daily snapshots
- **Configuration**: 
  - Before any configuration changes
  - Weekly automated backups

**Backup Verification:**

```bash
# Verify backup completion
aws backup list-backup-jobs \
  --by-state COMPLETED \
  --max-results 10

# Test restore procedure quarterly
# Restore to test environment and verify data integrity
```

## Credential and Key Rotation

This section provides step-by-step instructions for rotating programmatic system credentials and cryptographic keys used in Corridor deployments.

### Rotating Database Credentials

**Step 1: Create New Database User**

```bash
# Connect to RDS database
psql -h <rds-endpoint> -U corridor -d corridor

# Create new user with temporary password
CREATE USER corridor_new WITH PASSWORD 'NewSecurePassword123!';

# Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE corridor TO corridor_new;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO corridor_new;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO corridor_new;
```

**Step 2: Update Secrets Manager**

```bash
# Create new secret version with updated credentials
aws secretsmanager put-secret-value \
  --secret-id corridor/database/credentials \
  --secret-string '{"username":"corridor_new","password":"NewSecurePassword123!","host":"<rds-endpoint>","port":"5432","database":"corridor"}'
```

**Step 3: Update Application Configuration**

**For EKS:**
```bash
# Update Kubernetes secret
kubectl create secret generic corridor-db-credentials \
  --from-literal=username=corridor_new \
  --from-literal=password=NewSecurePassword123! \
  --from-literal=host=<rds-endpoint> \
  --namespace corridor \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart pods to pick up new credentials
kubectl rollout restart deployment -n corridor
```

**For ECS:**
```bash
# Update task definition with new secret ARN (if using Secrets Manager integration)
# Task definition automatically retrieves latest secret version
aws ecs update-service \
  --cluster corridor-cluster \
  --service corridor-service \
  --force-new-deployment
```

**For EC2:**
```bash
# Update configuration file
sudo vi /opt/corridor/instances/default/config/api_config.py
# Update SQLALCHEMY_DATABASE_URI with new credentials

# Restart services
sudo systemctl restart corridor-app corridor-api
```

**Step 4: Verify Application Connectivity**

```bash
# Test database connection
curl https://corridor.example.com/health

# Check application logs for connection errors
# For EKS: kubectl logs -n corridor deploy/corridor-app --tail=100
# For ECS: aws logs tail /ecs/corridor --follow
# For EC2: sudo journalctl -u corridor-app -n 100
```

**Step 5: Remove Old Database User**

```bash
# After verifying new credentials work (wait 24-48 hours)
psql -h <rds-endpoint> -U corridor_new -d corridor

# Revoke permissions from old user
REVOKE ALL PRIVILEGES ON DATABASE corridor FROM corridor;
REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM corridor;

# Drop old user
DROP USER corridor;
```

### Rotating AWS Access Keys

**Step 1: Create New Access Key**

```bash
# Create new IAM user access key
aws iam create-access-key --user-name corridor-service-user

# Save new access key ID and secret access key securely
```

**Step 2: Update Application Configuration**

```bash
# Update AWS credentials in Secrets Manager
aws secretsmanager put-secret-value \
  --secret-id corridor/aws/credentials \
  --secret-string '{"access_key_id":"AKIAIOSFODNN7EXAMPLE","secret_access_key":"wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"}'
```

**Step 3: Deploy Updated Configuration**

```bash
# Restart application to pick up new credentials
# For EKS: kubectl rollout restart deployment -n corridor
# For ECS: aws ecs update-service --cluster corridor-cluster --service corridor-service --force-new-deployment
# For EC2: sudo systemctl restart corridor-app
```

**Step 4: Verify New Credentials Work**

```bash
# Test AWS API calls with new credentials
aws s3 ls s3://corridor-backups-<unique-id>/ --profile new-credentials
```

**Step 5: Deactivate Old Access Key**

```bash
# Deactivate old access key
aws iam update-access-key \
  --user-name corridor-service-user \
  --access-key-id <old-access-key-id> \
  --status Inactive

# After verification period (24-48 hours), delete old key
aws iam delete-access-key \
  --user-name corridor-service-user \
  --access-key-id <old-access-key-id>
```

### Rotating SSL/TLS Certificates

**For ACM Certificates:**

```bash
# Request new certificate
aws acm request-certificate \
  --domain-name corridor.example.com \
  --validation-method DNS \
  --region us-east-1

# Complete DNS validation
# Update ALB listener to use new certificate
aws elbv2 modify-listener \
  --listener-arn <listener-arn> \
  --certificates CertificateArn=<new-certificate-arn>
```

**For cert-manager (EKS):**

```bash
# Certificates are automatically renewed by cert-manager
# Verify certificate status
kubectl get certificate -n corridor

# Force renewal if needed
kubectl delete secret tls-corridor-cert -n corridor
# cert-manager will automatically create new certificate
```

### Rotating Application API Keys

**Step 1: Generate New API Key**

```bash
# Generate new API key in Corridor application
# Navigate to: Settings → API Keys → Generate New Key
```

**Step 2: Update External Integrations**

```bash
# Update API key in external systems
# Update Secrets Manager if storing API keys there
aws secretsmanager put-secret-value \
  --secret-id corridor/api-keys \
  --secret-string '{"api_key":"new-api-key-value"}'
```

**Step 3: Revoke Old API Key**

```bash
# Revoke old API key in Corridor application
# Navigate to: Settings → API Keys → Revoke Key
```

### Rotation Schedule Recommendations

- **Database Credentials**: Every 90 days
- **AWS Access Keys**: Every 90 days
- **SSL/TLS Certificates**: Automatically renewed (ACM/cert-manager)
- **Application API Keys**: Every 180 days or when compromised
- **Container Registry Credentials**: Every 90 days

## Software Patches and Upgrades

This section provides prescriptive guidance for applying software patches and performing upgrades to Corridor deployments on AWS.

### Patch Management Strategy

**Patch Categories:**

1. **Security Patches**: Critical security vulnerabilities (apply immediately)
2. **Bug Fixes**: Application bug fixes (apply within 30 days)
3. **Feature Updates**: New features and enhancements (plan and schedule)
4. **Infrastructure Updates**: AWS service updates, OS patches (apply monthly)

### Pre-Patch Preparation

**Step 1: Review Patch Notes**

- Review Corridor release notes for changes and breaking changes
- Review AWS service updates and deprecations
- Identify dependencies and compatibility requirements

**Step 2: Create Backup**

```bash
# Create database snapshot
aws rds create-db-snapshot \
  --db-snapshot-identifier pre-patch-backup-$(date +%Y%m%d) \
  --db-instance-identifier corridor-db

# Backup configuration files
# (See Backup and Recovery section for detailed procedures)
```

**Step 3: Test in Non-Production Environment**

- Deploy patch to development/staging environment first
- Verify functionality and performance
- Document any issues or workarounds

### Applying Application Updates

**For EKS Deployments:**

```bash
# Step 1: Update container images
# Pull new container image version
docker pull <registry>/corridor/ggx:<new-version>

# Step 2: Update Kubernetes deployment
kubectl set image deployment/corridor-app \
  corridor-app=<registry>/corridor/ggx:<new-version> \
  -n corridor

kubectl set image deployment/corridor-api \
  corridor-api=<registry>/corridor/ggx:<new-version> \
  -n corridor

# Step 3: Monitor rollout
kubectl rollout status deployment/corridor-app -n corridor
kubectl rollout status deployment/corridor-api -n corridor

# Step 4: Verify application health
curl https://corridor.example.com/health

# Step 5: Rollback if needed
kubectl rollout undo deployment/corridor-app -n corridor
```

**For ECS Fargate Deployments:**

```bash
# Step 1: Register new task definition with updated image
aws ecs register-task-definition \
  --cli-input-json file://corridor-task-definition-v2.json

# Step 2: Update service with new task definition
aws ecs update-service \
  --cluster corridor-cluster \
  --service corridor-service \
  --task-definition corridor-task:v2 \
  --force-new-deployment

# Step 3: Monitor deployment
aws ecs describe-services \
  --cluster corridor-cluster \
  --services corridor-service \
  --query 'services[0].deployments'

# Step 4: Verify application health
curl https://corridor.example.com/health

# Step 5: Rollback if needed
aws ecs update-service \
  --cluster corridor-cluster \
  --service corridor-service \
  --task-definition corridor-task:v1
```

**For EC2 Deployments:**

```bash
# Step 1: Download new installation bundle
wget https://<download-url>/corridor-bundle-<new-version>.zip

# Step 2: Stop services
sudo systemctl stop corridor-app corridor-api corridor-worker-api

# Step 3: Backup current installation
sudo cp -r /opt/corridor /opt/corridor-backup-$(date +%Y%m%d)

# Step 4: Extract new bundle
cd /tmp
unzip corridor-bundle-<new-version>.zip

# Step 5: Run database migrations
/opt/corridor/venv-api/bin/corridor-api db upgrade

# Step 6: Restart services
sudo systemctl start corridor-app corridor-api corridor-worker-api

# Step 7: Verify application health
curl https://corridor.example.com/health

# Step 8: Rollback if needed
sudo systemctl stop corridor-app corridor-api
sudo rm -rf /opt/corridor
sudo cp -r /opt/corridor-backup-$(date +%Y%m%d) /opt/corridor
sudo systemctl start corridor-app corridor-api
```

### Applying Infrastructure Patches

**RDS Database Engine Updates:**

```bash
# Step 1: Check available engine versions
aws rds describe-db-engine-versions \
  --engine postgres \
  --engine-version 14.9 \
  --query 'DBEngineVersions[*].EngineVersion'

# Step 2: Apply minor version update during maintenance window
aws rds modify-db-instance \
  --db-instance-identifier corridor-db \
  --engine-version 14.10 \
  --apply-immediately false

# Step 3: Monitor update progress
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].[DBInstanceStatus,PendingModifiedValues]'
```

**EKS Cluster Updates:**

```bash
# Step 1: Update EKS cluster version
aws eks update-cluster-version \
  --name corridor-cluster \
  --version 1.28

# Step 2: Update node group AMI
aws eks update-nodegroup-version \
  --cluster-name corridor-cluster \
  --nodegroup-name corridor-nodes \
  --release-version <new-release-version>
```

**EC2 Instance Updates:**

```bash
# Step 1: Install OS updates
sudo yum update -y  # Amazon Linux
# or
sudo apt-get update && sudo apt-get upgrade -y  # Ubuntu

# Step 2: Reboot if kernel updates were applied
sudo reboot
```

### Post-Patch Verification

After applying patches, verify the following:

- Application health endpoint returns healthy status
- All services are running correctly
- Database connectivity is working
- File storage is accessible
- User authentication works
- Critical functionality is operational
- Performance metrics are within normal ranges
- No errors in application logs

### Rollback Procedures

**If patch causes issues:**

1. **Stop the update process** (if in progress)
2. **Restore from backup** (database, configuration)
3. **Revert to previous version** (application code)
4. **Verify rollback success**
5. **Document issues** for future reference

## License Management

This section provides prescriptive guidance on managing Corridor software licenses and AWS service licenses.

### Corridor Software License Management

**License Types:**

- **Subscription License**: Annual or multi-year subscription
- **Perpetual License**: One-time purchase with optional maintenance
- **Trial License**: Time-limited evaluation license

**License Information Storage:**

```bash
# License information is typically stored in:
# - Application configuration files
# - Environment variables
# - Secrets Manager (for license keys)

# View current license information
# For EKS:
kubectl get configmap corridor-config -n corridor -o yaml | grep -i license

# For EC2:
cat /opt/corridor/instances/default/config/app_config.py | grep -i license
```

**License Renewal Process:**

1. **Monitor License Expiration:**
   - Check license expiration date in application settings
   - Set up alerts 30 days before expiration
   - Review license usage and compliance

2. **Renew License:**
   - Contact Corridor sales or account representative
   - Provide current license information
   - Receive new license key or activation code

3. **Update License:**
   ```bash
   # Update license in application configuration
   # For EKS: Update ConfigMap or Secret
   kubectl create secret generic corridor-license \
     --from-literal=license-key=<new-license-key> \
     --namespace corridor \
     --dry-run=client -o yaml | kubectl apply -f -
   
   # Restart application
   kubectl rollout restart deployment -n corridor
   
   # For EC2: Update configuration file
   sudo vi /opt/corridor/instances/default/config/app_config.py
   # Update LICENSE_KEY value
   sudo systemctl restart corridor-app
   ```

4. **Verify License Activation:**
   - Check application logs for license validation
   - Verify license status in application UI
   - Confirm all features are accessible

**License Compliance:**

- Track license usage against purchased licenses
- Monitor user counts and feature usage
- Generate license usage reports quarterly
- Ensure compliance with license terms

### AWS Service License Management

**AWS Services:**

- AWS services use pay-as-you-go pricing (no separate licenses)
- Some services have usage limits (see AWS Service Limits section)
- Reserved Instances provide cost savings but are not licenses

**Third-Party Software Licenses:**

- **PostgreSQL**: Open-source (no license required)
- **Redis**: Open-source (no license required)
- **Python**: Open-source (no license required)
- **Java**: Open-source OpenJDK (no license required)
- **Kubernetes**: Open-source (no license required)

**License Audit:**

- Conduct quarterly license audits
- Document all software licenses and expiration dates
- Maintain license inventory spreadsheet
- Set up renewal reminders

## AWS Service Limits Management

This section provides prescriptive guidance on managing AWS service limits (quotas) to ensure deployments can scale and operate effectively.

### Understanding AWS Service Limits

**Common Service Limits:**

- **EC2 Instances**: Number of running instances per region
- **EKS Clusters**: Number of clusters per account
- **RDS Instances**: Number of DB instances per region
- **VPCs**: Number of VPCs per region
- **Elastic IPs**: Number of Elastic IPs per region
- **NAT Gateways**: Number of NAT Gateways per availability zone

### Checking Current Service Limits

**Step 1: List Service Quotas**

```bash
# List all service quotas for a specific service
aws service-quotas list-service-quotas \
  --service-code ec2 \
  --query 'Quotas[*].[QuotaName,Value,Adjustable]' \
  --output table

# Check specific quota
aws service-quotas get-service-quota \
  --service-code ec2 \
  --quota-code L-0263D0A3  # Running On-Demand EC2 instances
```

**Step 2: Monitor Quota Usage**

```bash
# Get current usage
aws service-quotas get-aws-default-service-quota \
  --service-code ec2 \
  --quota-code L-0263D0A3

# Set up CloudWatch alarms for quota usage
aws cloudwatch put-metric-alarm \
  --alarm-name ec2-instance-quota-warning \
  --alarm-description "Alert when EC2 instance quota exceeds 80%" \
  --metric-name ResourceCount \
  --namespace AWS/Usage \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### Requesting Limit Increases

**Step 1: Identify Required Increase**

- Determine current usage and projected growth
- Calculate required limit increase
- Document business justification

**Step 2: Submit Limit Increase Request**

```bash
# Request limit increase via AWS CLI
aws service-quotas request-service-quota-increase \
  --service-code ec2 \
  --quota-code L-0263D0A3 \
  --desired-value 100

# Or use AWS Console:
# Service Quotas → AWS services → Select service → Request quota increase
```

**Step 3: Monitor Request Status**

```bash
# Check request status
aws service-quotas list-requested-service-quota-change-history \
  --service-code ec2 \
  --query 'RequestedQuotas[*].[QuotaName,Status,DesiredValue]' \
  --output table
```

**Step 4: Implement Workarounds (If Needed)**

- Use multiple AWS accounts for different environments
- Distribute resources across multiple regions
- Use Spot Instances for non-production workloads
- Optimize resource usage

### Proactive Limit Management

**Best Practices:**

1. **Monitor Quota Usage Regularly:**
   - Set up CloudWatch alarms at 80% usage
   - Review quota usage monthly
   - Plan for growth

2. **Request Increases Early:**
   - Request increases 2-4 weeks before needed
   - Provide business justification
   - Request slightly higher than immediate need

3. **Document Limits:**
   - Maintain inventory of all service limits
   - Track limit increase requests
   - Document approved limits

4. **Optimize Resource Usage:**
   - Right-size instances and resources
   - Use Reserved Instances for predictable workloads
   - Clean up unused resources regularly

## Fault Handling and Recovery

This section provides step-by-step instructions for handling fault conditions and recovering the Corridor software deployment.

### Handling Fault Conditions

#### Fault Detection

**Step 1: Identify Fault Type**

Common fault conditions:
- Application unresponsive or returning errors
- Database connection failures
- Storage access issues
- Network connectivity problems
- High resource utilization
- Service crashes or restarts

**Step 2: Check Application Health**

```bash
# Check health endpoint
curl https://corridor.example.com/health

# Check load balancer target health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>

# Check application logs for errors
# For EKS:
kubectl logs -n corridor deploy/corridor-app --tail=100 | grep -i error

# For ECS:
aws logs tail /ecs/corridor --follow | grep -i error

# For EC2:
sudo journalctl -u corridor-app -n 100 | grep -i error
```

**Step 3: Check Infrastructure Health**

```bash
# Check database status
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].[DBInstanceStatus,DBInstanceStatusInfos]'

# Check compute resources
# For EKS:
kubectl get nodes
kubectl get pods -n corridor

# For ECS:
aws ecs describe-tasks \
  --cluster corridor-cluster \
  --tasks $(aws ecs list-tasks --cluster corridor-cluster --query 'taskArns[0]' --output text)

# For EC2:
aws ec2 describe-instance-status --instance-ids <instance-id>
```

#### Common Fault Scenarios and Resolution

**Scenario 1: Application Pod/Container Crashes**

**Symptoms:** Pods/containers restarting frequently, application unavailable

**Resolution Steps:**

```bash
# For EKS:
# 1. Check pod status
kubectl get pods -n corridor

# 2. Describe pod for events
kubectl describe pod <pod-name> -n corridor

# 3. Check pod logs
kubectl logs <pod-name> -n corridor --previous

# 4. Check resource limits
kubectl top pod <pod-name> -n corridor

# 5. Scale up if resource constrained
kubectl scale deployment corridor-app --replicas=3 -n corridor

# For ECS:
# 1. Check task status
aws ecs describe-tasks --cluster corridor-cluster --tasks <task-id>

# 2. Check task logs
aws logs tail /ecs/corridor --follow

# 3. Update service desired count
aws ecs update-service --cluster corridor-cluster --service corridor-service --desired-count 3

# For EC2:
# 1. Check service status
sudo systemctl status corridor-app

# 2. Check service logs
sudo journalctl -u corridor-app -n 100

# 3. Restart service
sudo systemctl restart corridor-app
```

**Scenario 2: Database Connection Failures**

**Symptoms:** Application cannot connect to database, database errors in logs

**Resolution Steps:**

```bash
# 1. Verify database is running
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].DBInstanceStatus'

# 2. Check database endpoint
aws rds describe-db-instances \
  --db-instance-identifier corridor-db \
  --query 'DBInstances[0].Endpoint.Address'

# 3. Test database connectivity
psql -h <rds-endpoint> -U corridor -d corridor -c "SELECT 1;"

# 4. Check security groups
aws ec2 describe-security-groups --group-ids <db-sg-id>

# 5. Verify credentials in Secrets Manager
aws secretsmanager get-secret-value --secret-id corridor/database/credentials

# 6. Restart application to refresh connections
# For EKS: kubectl rollout restart deployment -n corridor
# For ECS: aws ecs update-service --cluster corridor-cluster --service corridor-service --force-new-deployment
# For EC2: sudo systemctl restart corridor-app
```

**Scenario 3: Storage Access Issues**

**Symptoms:** File uploads/downloads failing, storage errors

**Resolution Steps:**

```bash
# For EFS:
# 1. Check EFS status
aws efs describe-file-systems --file-system-id <efs-id>

# 2. Check mount targets
aws efs describe-mount-targets --file-system-id <efs-id>

# 3. Test mount from application
# For EKS:
kubectl exec -it -n corridor deploy/corridor-app -- df -h | grep efs

# For ECS:
aws ecs execute-command --cluster corridor-cluster --task <task-id> --container corridor-app --command "df -h"

# For EBS (EC2):
# 1. Check volume status
aws ec2 describe-volumes --volume-ids <volume-id>

# 2. Check volume attachment
aws ec2 describe-instances --instance-ids <instance-id> --query 'Instances[0].BlockDeviceMappings'

# 3. Check filesystem
df -h
sudo mount /dev/xvdf /mnt/data
```

**Scenario 4: High Resource Utilization**

**Symptoms:** Slow response times, timeouts, high CPU/memory usage

**Resolution Steps:**

```bash
# 1. Check resource utilization
# For EKS:
kubectl top nodes
kubectl top pods -n corridor

# For ECS:
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ServiceName,Value=corridor-service \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average,Maximum

# 2. Scale resources
# For EKS: Scale node group or increase pod replicas
aws eks update-nodegroup-config \
  --cluster-name corridor-cluster \
  --nodegroup-name corridor-nodes \
  --scaling-config minSize=5,maxSize=15

# For ECS: Increase task count
aws ecs update-service \
  --cluster corridor-cluster \
  --service corridor-service \
  --desired-count 4

# For EC2: Upgrade instance type or add instances
aws ec2 modify-instance-attribute \
  --instance-id <instance-id> \
  --instance-type Value=t3.2xlarge
```

### Software Recovery Procedures

#### Complete Deployment Recovery

**Step 1: Assess Recovery Requirements**

- Identify what needs to be recovered (database, files, configuration)
- Determine recovery point objective (RPO) and recovery time objective (RTO)
- Choose recovery method (full restore, partial restore, failover)

**Step 2: Restore Infrastructure (If Needed)**

```bash
# Restore from Infrastructure-as-Code
# Using Terraform:
terraform apply -var-file=production.tfvars

# Using CloudFormation:
aws cloudformation create-stack \
  --stack-name corridor-recovery \
  --template-body file://corridor-infrastructure.yaml
```

**Step 3: Restore Database**

```bash
# Restore from latest snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier corridor-db-recovered \
  --db-snapshot-identifier corridor-db-snapshot-20240101

# Wait for restore completion
aws rds wait db-instance-available \
  --db-instance-identifier corridor-db-recovered

# Update application configuration with new database endpoint
```

**Step 4: Restore File Storage**

```bash
# Restore EFS from backup
aws backup start-restore-job \
  --recovery-point-arn <recovery-point-arn> \
  --iam-role-arn arn:aws:iam::<account-id>:role/service-role/AWSBackupDefaultServiceRole \
  --resource-type EFS \
  --metadata file-system-id=<efs-id>

# Or restore EBS from snapshot
aws ec2 create-volume \
  --snapshot-id <snapshot-id> \
  --availability-zone us-east-1a
```

**Step 5: Restore Application Configuration**

```bash
# Restore Kubernetes ConfigMaps/Secrets
kubectl apply -f corridor-configmaps-backup-20240101.yaml -n corridor

# Restore ECS task definition
aws ecs register-task-definition \
  --cli-input-json file://corridor-task-definition-backup-20240101.json

# Restore EC2 configuration files
tar -xzf corridor-config-backup-20240101.tar.gz -C /
```

**Step 6: Deploy Application**

```bash
# Deploy application using restored configuration
# For EKS:
kubectl apply -f corridor-manifests.yaml -n corridor

# For ECS:
aws ecs update-service \
  --cluster corridor-cluster \
  --service corridor-service \
  --task-definition corridor-task

# For EC2:
sudo systemctl start corridor-app corridor-api
```

**Step 7: Verify Recovery**

```bash
# Verify application health
curl https://corridor.example.com/health

# Verify database connectivity
psql -h <rds-endpoint> -U corridor -d corridor -c "SELECT COUNT(*) FROM users;"

# Verify file storage
# Test file upload/download functionality

# Verify all services
# Check application logs for errors
```

#### Disaster Recovery to Secondary Region

**Step 1: Prepare Secondary Region**

```bash
# Copy database snapshot to secondary region
aws rds copy-db-snapshot \
  --source-db-snapshot-identifier corridor-db-snapshot-20240101 \
  --target-db-snapshot-identifier corridor-db-snapshot-dr \
  --target-region us-west-2

# Copy EBS snapshots
aws ec2 copy-snapshot \
  --source-region us-east-1 \
  --source-snapshot-id <snapshot-id> \
  --region us-west-2
```

**Step 2: Deploy Infrastructure in Secondary Region**

```bash
# Deploy infrastructure using Terraform/CloudFormation
# Update region parameter to secondary region
terraform apply -var="aws_region=us-west-2"
```

**Step 3: Restore Data in Secondary Region**

```bash
# Restore database from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier corridor-db-dr \
  --db-snapshot-identifier corridor-db-snapshot-dr \
  --region us-west-2

# Restore file storage
# (Follow file storage restore procedures)
```

**Step 4: Update DNS for Failover**

```bash
# Update Route 53 health check and failover
aws route53 change-resource-record-sets \
  --hosted-zone-id <hosted-zone-id> \
  --change-batch file://failover-routing.json
```

### Recovery Testing

**Regular Recovery Testing:**

- Test database restore procedures quarterly
- Test file storage restore procedures quarterly
- Test complete deployment recovery annually
- Document test results and update procedures

## Support Information

This section provides details on how to receive support, technical support tiers, and Service Level Agreements (SLAs) for Corridor deployments on AWS.

### How to Receive Support

**Support Channels:**

1. **Email Support:**
   - Primary support email: support@corridorplatforms.com
   - Include deployment method (EKS/ECS/EC2), AWS region, error messages, and logs
   - Response time: Based on support tier (see below)

2. **Support Portal:**
   - Access support portal at: https://support.corridorplatforms.com
   - Submit tickets, track issues, access knowledge base
   - Available 24/7 for ticket submission

3. **Emergency Support:**
   - For critical production issues
   - Contact via emergency hotline (Premium/Enterprise tiers)
   - Available 24/7 for critical issues

**Information to Provide When Requesting Support:**

- Deployment method (EKS, ECS Fargate, or EC2)
- AWS region and account ID
- Corridor version
- Detailed error messages and logs
- Steps to reproduce the issue
- Screenshots or screen recordings (if applicable)
- Impact assessment (number of users affected, business impact)

### Technical Support Tiers

**Tier 1: Standard Support**

- **Availability**: Business hours (9 AM - 5 PM EST, Monday-Friday)
- **Response Time**: 
  - Critical: 8 business hours
  - High: 1 business day
  - Medium: 2 business days
  - Low: 3 business days
- **Channels**: Email, Support Portal
- **Included Services**:
  - Product documentation access
  - Knowledge base access
  - Bug fixes and security patches
  - General product questions
- **Exclusions**: 
  - Custom development
  - Architecture design consultation
  - On-site support

**Tier 2: Premium Support**

- **Availability**: Extended business hours (8 AM - 8 PM EST, Monday-Friday)
- **Response Time**:
  - Critical: 4 business hours
  - High: 8 business hours
  - Medium: 1 business day
  - Low: 2 business days
- **Channels**: Email, Support Portal
- **Included Services**:
  - All Standard Support services
  - Priority ticket handling
  - Architecture guidance
  - Performance optimization assistance
- **Additional Features**:
  - Monthly health check reviews
  - Proactive monitoring recommendations

**Tier 3: Enterprise Support**

- **Availability**: 24/7 support
- **Response Time**:
  - Critical: 1 hour (24/7)
  - High: 4 hours (24/7)
  - Medium: 8 business hours
  - Low: 1 business day
- **Channels**: Email, Support Portal, Emergency Hotline
- **Included Services**:
  - All Premium Support services
  - 24/7 critical issue support
  - Dedicated support engineer
  - Custom deployment assistance
  - Quarterly architecture reviews
  - On-site support (as needed)
- **Additional Features**:
  - Custom SLA definitions
  - Direct access to engineering team
  - Proactive issue identification

### Support Tiers and Service Level Agreements (SLAs)

**Severity Levels:**

1. **Critical (P1)**:
   - Production system down or severely degraded
   - Data loss or corruption risk
   - Security breach
   - **SLA**: 
     - Standard: 8 business hours
     - Premium: 4 business hours
     - Enterprise: 1 hour (24/7)

2. **High (P2)**:
   - Major feature unavailable
   - Significant performance degradation
   - **SLA**:
     - Standard: 1 business day
     - Premium: 8 business hours
     - Enterprise: 4 hours (24/7)

3. **Medium (P3)**:
   - Minor feature unavailable
   - Workaround available
   - **SLA**:
     - Standard: 2 business days
     - Premium: 1 business day
     - Enterprise: 8 business hours

4. **Low (P4)**:
   - General questions
   - Feature requests
   - **SLA**:
     - Standard: 3 business days
     - Premium: 2 business days
     - Enterprise: 1 business day

**SLA Guarantees:**

- **Response Time**: Time to initial response from support team
- **Resolution Time**: Target time to resolve issue (varies by severity and complexity)
- **Uptime Guarantee**: 99.9% availability (Enterprise tier)
- **Escalation Process**: Automatic escalation if SLA not met

**Support Coverage:**

- **Product Support**: Corridor platform functionality, deployment, configuration
- **Infrastructure Support**: AWS infrastructure guidance (limited)
- **Integration Support**: Third-party integration assistance
- **Exclusions**: 
  - Custom development
  - Training (available as separate service)
  - AWS account management

**Escalation Process:**

1. **Level 1**: Support Engineer (initial response)
2. **Level 2**: Senior Support Engineer (complex issues)
3. **Level 3**: Engineering Team (critical bugs, architecture issues)
4. **Level 4**: Product Management (feature requests, strategic issues)

**Support Request Process:**

1. Submit ticket via email or support portal
2. Receive ticket confirmation and tracking number
3. Initial response within SLA timeframe
4. Issue investigation and resolution
5. Ticket closure with resolution summary

**Contact Information:**

- **Support Email**: support@corridorplatforms.com
- **Support Portal**: https://support.corridorplatforms.com
- **Emergency Hotline**: Provided upon account activation (Enterprise)

## Installation Methods

Corridor supports three different installation approaches on AWS, each suited to different organizational needs and infrastructure preferences:

### Option 1: Kubernetes - EKS

Deploy Corridor on Amazon Elastic Kubernetes Service (EKS) for a cloud-native, containerized deployment.

**Best for:**

- Organizations with Kubernetes expertise
- Multi-tenant deployments with namespace isolation
- Auto-scaling and high availability requirements
- Modern cloud-native infrastructure

[View EKS Installation Guide →](./aws-eks.md)

### Option 2: Serverless - ECS Fargate

Deploy Corridor using AWS Fargate for a serverless container deployment.

**Best for:**

- Organizations wanting serverless infrastructure
- Minimal infrastructure management
- Variable workload patterns

[View Fargate Installation Guide →](./aws-fargate.md)

### Option 3: Virtual Machines - EC2

Deploy Corridor on Amazon EC2 instances for a traditional VM-based deployment.

**Best for:**

- Organizations preferring VM-based infrastructure
- Direct control over the operating system
- Traditional IT infrastructure patterns
- Custom hardware requirements

[View EC2 Installation Guide →](./aws-ec2.md)

## Common AWS Services

All deployment options utilize these AWS managed services:

- **RDS**: PostgreSQL database for metadata storage
- **S3**: Object storage for file management (or EFS for NFS)
- **Application Load Balancer**: HTTP(S) load balancing
- **Route 53**: Domain name management
- **VPC**: Virtual private cloud networking

## Choosing the Right Option

| Factor                         | EKS (Kubernetes)    | ECS Fargate | EC2 (VMs)    |
| ------------------------------ | ------------------- | ----------- | ------------ |
| **Complexity**                 | Higher              | Medium      | Lower        |
| **Scalability**                | Automatic           | Automatic   | Manual       |
| **Multi-tenancy**              | Native (namespaces) | Task-based  | Separate VMs |
| **Operational Overhead**       | Lower (managed K8s) | Lowest      | Higher       |
| **Deployment Speed**           | Fast                | Fastest     | Moderate     |
| **Infrastructure Management**  | Minimal             | None        | Full         |
| **Cost Model**                 | Node-based          | Per task    | Per instance |
| **Kubernetes Skills Required** | Yes                 | No          | No           |
