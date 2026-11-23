---
title: "System Health"
description: "Read server load, disks, installed software, processes and the Python kernel pool in GGX System Health, and download a diagnostic bundle for support."
---

**System Health** shows the server that GGX runs on. Use it first when GGX feels slow or a job fails. Only users with the **Organization Admin** permission can open it. Go to **Org Settings**, then **System → System Health**.

## What the page shows

| Card | Contents |
|------|----------|
| **Load of the server** | CPU and memory in use, each with a trend of the last minutes, and the free space on each disk. It updates every 10 seconds, and the refresh button reads it again. The host name and the number of logical cores appear here. |
| **Operating system** | Name, kernel version and architecture. |
| **Installation** | How GGX was installed, such as a Docker container, a Kubernetes pod or an Amazon EC2 server, and whether the cloud is AWS, Google Cloud or Azure. The signs GGX used to decide are listed under it. |
| **Software** | The Python version and the GGX version. **All GGX packages** opens a table of every package and its version. |
| **Processes** | The GGX services running on this server, with their PID, status, start time and memory. |
| **Kernel pool** | The Python processes that run chats, jobs and simulations. They start when needed. Each row says what it is used for and whether it is in use or free. |

:::note
In a container, the load and disk figures are those of the server, not the limits of the container.
:::

A process missing from **Processes** may run on another server, or may have stopped. The page lists only this server.

## Download a diagnostic bundle

The **Diagnostic bundle** card makes one zip file for the GGX support team. It holds the errors, the slow requests, the settings and the end of the logs for the period. It holds no data from your projects and no passwords, keys or tokens.

1. Choose **Last day**, **Last 3 days** or **Last 7 days**.
2. Click **Download**.
3. Send the file to support as it is.

If the bundle fails, try again or choose a shorter period. The card works even when the rest of the page cannot read the server.

See also: [Platform settings](/administration/platform-settings/) and [Self-hosting](/technology/self-hosting/).
