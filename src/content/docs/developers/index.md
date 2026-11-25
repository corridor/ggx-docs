---
title: "Developers"
description: "Work with GGX from code: the Python SDK, the ggx command, MCP for coding agents, and how GGX reads agent code from a Code Repo."
---

GGX has a web interface, and it also has interfaces for code. This section covers the ones that run outside the browser.

| Interface | Use it to | Page |
| --- | --- | --- |
| **Python SDK** (`genguardx`) | Read registered objects, fetch datasets, read simulation results and deployment logs from Python. | [Python SDK reference](./sdk/) |
| **GGX Sync** and the `ggx` command | Declare prompts, models, RAGs, agents, global functions and reports in code and push them to GGX. | [GGX Sync](../register-and-refine/sync/) |
| **MCP server** | Let a coding agent such as Claude Code or Codex find, author and evaluate GGX objects. | [Connect GGX with MCP](../integrations/mcp/) |
| **Code Repos** | Run an agent whose code lives in a Git repository, with GGX showing what the code is made of. | [How GGX reads agent code](./code-repo-agents/) |
| **Export bundle** | Take an approved agent out of GGX to run it elsewhere. | [CI/CD and Direct to Production](../deploy-and-monitor/direct-to-production/) |

All of them act as a GGX user, so they see only what that user can see.
