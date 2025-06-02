# Scalability and Sizing

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

The simulations and other jobs like Comparison, Validation, etc. Use the Celery workers to perform tasks. There are 2 parts which can be considered here:

- Number of parallel jobs to run
- Cluster nodes available for use per job

If the number of parallel jobs is a concern, due to a large job blocking the queue of later jobs, etc. - this can be handled by adding more "Spark - Celery Workers" as needed. The Celery Workers are stateless and all state is maintained in the Task Messaging queue (Redis) and removing/adding more is seamless. Note that adding too many Spark - Celery workers could cause resource contention between the workers themselves and may require an increase in cluster nodes.

If the spark jobs themselves are slow - then the issue is more likely the cluster nodes available per job. i.e. the number of Spark workers or YARN containers that are allocated per job. To make this faster, more spark nodes need to be provided to make Spark jobs run faster.

## User-initiated analytics

The platform's Notebook section allows the user to initiate their own jobs in a free-form manner using Python/PySpark. As these jobs are user-dependent, they can utilize a large number of cluster resources if not used correctly. If this causes issues with the Simulation jobs, it is recommended to use separate YARN queues to manage the resource allocation appropriately.

## Application

The Application's scalability is an important factor to consider when the number of concurrent users starts increasing over time. This can impact the usability of the application itself and can be scaled by identifying which portion of the application is causing the bottleneck. The Metadata
Database or the API Server could be the cause of issues here. It can be easily rectified by adding more resources to these components or parallelizing them with Database Read Replicas or API Servers
appropriately.

!!! note

    The API Servers are stateless and can be easily scaled up/down as needed.
