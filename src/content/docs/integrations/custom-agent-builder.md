---
title: "Custom agent builder"
description: "Connect an agent studio GGX does not support by writing up to five short Python functions that list, call, describe, replace, and update its agents."
---

Use a custom agent builder when your agents are built in a system GGX has no integration for, such as an in-house platform. GGX talks to an agent builder through five things. You write each one as a short Python function that calls your builder and returns the answer in a standard shape.

This is an escape hatch. Prefer a built-in [agent studio](../agent-studios/) when one exists.

## The five functions

| Part | Function | GGX uses it to | Needed |
| --- | --- | --- | --- |
| List the agents | `list_agents()` | Show the agents of your builder | Yes |
| Invoke an agent | `invoke_agent(agent_id, messages, session_id=None)` | Send a conversation to an agent and get its answer | Yes |
| Describe what the agent is made of | `describe_agent(agent_id)` | Read an agent's instruction, model, knowledge, tools, and guardrails | No |
| Run with AI components replaced | `run_with_replacements(agent_id, messages, replacements)` | Try another prompt or model, or mock a tool or knowledge, for one run | No |
| Create or update the agent | `update_agent(agent_id, changes)` | Change an agent in your builder, or create one | No |

Every function takes plain JSON values by name and returns JSON. The dialog shows the inputs and the expected output of each part, with an example and a working skeleton.

- **List** returns agents with `id`, `name`, and `status`. `version`, `model`, and `description` are optional.
- **Invoke** returns an OpenAI chat completion. GGX reads the answer from `choices[0].message.content`.
- **Describe** returns what your builder has and leaves out the rest.
- **Replace** returns the completion and an `applied` list of the parts the run really used. List only what your builder overrode.
- **Update** returns what changed, with the value before and after, so GGX can show it and undo it. Use an agent ID of `None` to create.

## How to set one up

1. Store the keys first. In **Org Settings**, open **Advanced** and add the URL and key of your builder as environment variables, for example `MY_BUILDER_URL` and `MY_BUILDER_API_KEY`.
2. Open **Org Settings → Integrations → Agent Studios** and select **Other agent studio**, then **Add**.
3. Enter a **Name**. Every custom builder has the same icon in the list, so the name tells them apart.
4. For each part, select **Set up**. Replace the skeleton's canned answer with a call to your builder, and map its answer to the standard shape. Read keys with `os.environ["MY_BUILDER_API_KEY"]`.
5. Select **Test**. GGX runs the function with the example input on a Python kernel. Edit the JSON to use a real agent ID. The result shows what GGX reads, what the function printed, or the error, and a test stops after 60 seconds. Nothing is saved by a test.
6. Save.

Turn **Enabled** off to keep a draft. A draft can hold any parts, but enabling the connector needs **List** and **Invoke**.

## Notes

- Never write keys, tokens, or passwords in the code or the test input. Anyone with read access to organization settings can read the code, and a test's output is shown to whoever runs it.
- Only people who can change organization settings can edit, test, or remove a connector.
- Give the builder's key only the rights the functions need: read for List, Describe, and Invoke, and write only if you set up Update.
- The kernel has the packages every GGX Python kernel has, such as `httpx2`, and none from a project. A missing function name, or a return value that is not the standard shape, is reported when you test or save.
- A custom connector is saved and tested in Org Settings. GGX does not call your builder when you save.
