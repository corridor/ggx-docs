---
title: "How GGX reads agent code"
description: "How GGX finds agents in a Code Repo, what it can and cannot read from the code, and why a detected value can be shown as not known."
---

When an agent runs code from a [Code Repo](../../register-and-refine/inventory-management/#code-repos), GGX reads the code to find the agent and to show what it is made of. This page describes what you see and what GGX can and cannot work out.

GGX reads the Python files as text. It does not import or run them, and it does not build an environment, so it is safe to point at any repository.

## Pick an agent from the repository

When you create an agent of type **Code Repo**, choose the repository and branch. GGX scans the branch and offers the agents it finds under **Pick from detected agents**. Choose one, or choose **Provide manually**. See [Use a Code Repo as an agent](../../register-and-refine/inventory-management/#use-a-code-repo-as-an-agent) for the full steps and the supported frameworks.

An agent is listed when:

- it is assigned to a name at the top level of a file, because that name is what GGX imports to run it, or
- a function with no required arguments returns it, because GGX calls that function once to get the agent.

An agent built inside a function that does not return it, or passed straight into another call, is not listed. Classes that are not yet an agent are not listed either. If your agent is missing, expose it as a top-level variable or a factory function, or use **Provide manually**.

GGX recognises more frameworks than it can run. Agents of a framework GGX cannot run are shown as **not supported yet**.

## See what an agent is made of

In the **Precedents** view of a Code Repo agent's **Lineage** section, GGX shows the models, prompts, tools, knowledge sources and sub-agents it detected in the code, next to the GGX objects the agent uses. Select one to see its file, lines and value. [Lineage Tracking](../../register-and-refine/lineage-tracking/#assets-detected-in-agent-code) describes the nodes and their details.

Detected nodes are not GGX objects. They have no page, status or approval. If a detected model or prompt matches one registered in GGX, GGX shows the registered object instead of a duplicate. The match is exact: a model by its name, a prompt by its text. A near miss stays detected.

## Why a value is not known

GGX never guesses. When it cannot read a value from the code, it says why:

| Reason shown | Meaning |
| --- | --- |
| built when the code runs | The value is an f-string, a call or similar |
| set by an environment variable | The value comes from the environment |
| read from a file when the code runs | The value is loaded from a file |
| a parameter of a function | The caller supplies the value |
| defined in another file | The definition is outside the files GGX could follow |
| several values are possible | The code gives more than one answer |
| too many steps to follow | The value is passed through more steps than GGX follows |
| hidden on purpose | A key, token or password. GGX never copies these. |

GGX follows names inside a file and across the files of the repository, so a prompt defined as a constant in one file and used in another is found.

## Detection is read-only

Nothing is stored. GGX reads the commit when the Precedents view loads, and again when you refresh it. If the repository or branch cannot be read, the lineage shows a message that the code could not be read at that commit, and the rest of the page keeps working.

## Related

- [Agents](../../register-and-refine/inventory-management/pipelines/) for how to create an agent.
- [Lineage Tracking](../../register-and-refine/lineage-tracking/) for the Lineage section.
