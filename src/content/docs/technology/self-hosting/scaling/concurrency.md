---
title: "Concurrency"
description: "Increase the number of parallel GGX runs by sizing the kernel worker, the kernel limits, the job queue, and the environments on the shared disk."
---

All the Python that GGX runs for its users, including the background jobs (simulations and annotation queue ingestions), executes in Jupyter kernels that belong to the **kernel worker** (`corridor-worker run`). How many things can run in parallel is decided by the limits of the kernel runtime. See [Kernel Runtime](../../configurations/process-management/#kernel-runtime) for what the runtime is and how to run it.

## Limits

Set these in `api_config.py` (or as environment variables with the `CORRIDOR_` prefix):

- `KERNEL_MAX_PROCESSES` (default `4`): The number of kernels that can run at the same time, across all API workers.
- `KERNEL_MAX_JOB_PROCESSES` (default `2`): Of those kernels, the number that can run background jobs at the same time. The other kernels stay available for chats, Debug Code, deployments, figures, and data previews.
- `KERNEL_MAX_TEST_GENERATION_PROCESSES` (default `2`): Of those kernels, the number that can run the tests that Corra generates for a feedback portal.
- `KERNEL_IDLE_TIMEOUT` (default 15 minutes, in seconds): How long a kernel that is not in use is kept before it is stopped.
- `JOB_TIME_LIMIT` (default 2 hours, in seconds): How long a background job can run.

When all the kernels that a job may use are busy, new jobs wait in a queue and start in the order in which they were submitted. A chat turn waits for a kernel for as long as it takes. A short request, such as a figure or a data preview, gives up after 60 seconds and says that every kernel is busy.

## Sizing

Each kernel is a Python process with the packages of its project, so its memory is whatever the code and the data in it need. To allow more parallel runs, raise `KERNEL_MAX_PROCESSES` (and `KERNEL_MAX_JOB_PROCESSES` for jobs) together with the CPU and memory of the machine or pod that runs the kernel worker, and restart the processes.

The kernels are shared by all the API workers, so running more API workers does not add kernels. To run more kernels at once, raise `KERNEL_MAX_PROCESSES` and give the kernel worker the memory and CPU for them.

The environments with the Python packages of each project are built the first time they are needed, which can take a while for large projects, and are kept on the shared disk for 14 days after their last use.
