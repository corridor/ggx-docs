# Scalability and Sizing
Source: https://docs.genguardx.ai/technology/self-hosting/scaling/scalability/
Markdown: https://docs.genguardx.ai/technology/self-hosting/scaling/scalability/index.md
Description: Plan self-hosted GGX scalability for production throughput, simulation jobs, user analytics, application services, databases, APIs, and worker capacity.

If the platform seems to be slow, there may be an infrastructure constraint in terms of resources
that could be causing this. This section describes how different aspects of scalability have been
kept in mind when designing the platform.

The way to think about scalability in the platform is:

- Production
- Simulation and other jobs
- User-initiated analytics
- Application

## Production

The production scalability again can be thought of in two parts:

- Time to execute the artifact-bundle/policy
- Throughput for the production orchestration

The time taken for the artifact-bundle depends on the complexity of the logic written in the platform. This can be sped up by writing more efficient codes or simplifying the logic.

The throughput for the orchestrations depends on the method of deployment of the Production layer, whether it is an HTTP API, serverless architecture, python runtime execution, etc.

## Simulation and other jobs

Simulations and the other background jobs, such as annotation queue ingestions, run in Jupyter kernels that belong to the kernel worker. There are 2 parts which can be considered here:

- Number of parallel jobs to run
- Resources available to each job

If the number of parallel jobs is a concern, due to a large job blocking later jobs, increase `KERNEL_MAX_JOB_PROCESSES` (and `KERNEL_MAX_PROCESSES` with it). Note that too many parallel jobs can cause resource contention between them, so increase the CPU and memory of the machine or pod that runs the kernel worker as well. Jobs wait in a queue when the limit is reached and start in order. See [Concurrency](https://docs.genguardx.ai/technology/self-hosting/scaling/concurrency/) for the settings.

If the jobs themselves are slow, the cause is more likely the CPU and memory that each kernel gets, or the efficiency of the logic and the size of the data.

## User-initiated analytics

Chats, Debug Code, figures, and data previews run in the same kernels as the jobs, within the `KERNEL_MAX_PROCESSES` limit and with a share kept apart for jobs (`KERNEL_MAX_JOB_PROCESSES`), so a burst of long jobs does not take every kernel away from interactive work. Idle kernels are stopped after `KERNEL_IDLE_TIMEOUT`.

## Application

The Application's scalability is an important factor to consider when the number of concurrent users starts increasing over time. This can impact the usability of the application itself and can be scaled by identifying which portion of the application is causing the bottleneck. The Metadata
Database or the API Server could be the cause of issues here. It can be easily rectified by adding more resources to these components or parallelizing them with Database Read Replicas or API Servers
appropriately.

**Note**

The API Servers are stateless and can be easily scaled up/down as needed.
