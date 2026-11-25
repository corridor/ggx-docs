---
title: "Chat and activity"
description: "Open Corra AI from the top bar, chat with it, and follow the runs and chats it keeps for you in the activity drawer."
---

The **Corra AI** button in the top bar is the front door to Corra. It opens a drawer that lists your Corra runs and chats, and from there you start a chat. This page covers the drawer and the general chat.

## Open the activity drawer

Click the sparkle button named **Corra AI** in the top bar. A number on the button counts the runs that are working now. The tooltip reads "Corra AI: 2 running" in that case.

The drawer lists, newest first:

- **Runs**: background jobs that Corra started for you, such as an issue finder run, a risk assessment fill or test generation.
- **Chats**: your conversations with Corra, including the discussions about an issue and the general chat.

Each item shows a title, the object it belongs to, how long ago it last changed and, for a chat, the number of messages. A run has a tag: **Running**, **Done**, **Failed** or **Stopped**. A running run also shows what it is doing now.

| Control | What it does |
|---------|--------------|
| **All**, **Running**, **Runs**, **Chats** | Filters the list. |
| Refresh button | Reads the list again. The drawer also refreshes itself every few seconds while it is open. |
| **New chat** | Closes the drawer and opens an empty chat. |
| **Open** | Opens the object the item belongs to. For an issue, it opens that issue. |
| **Open chat** | Opens the general chat. |

The drawer shows the latest 50 items and says "Showing the latest 50." when there are more. Only your own runs and chats are listed. An empty drawer says "Nothing here yet. Runs and chats with Corra AI show up here."

## Chat with Corra

Click **New chat** or **Open chat**. The chat opens as a panel on the right of the page, titled **CORRA**. Type in the box ("Type a message…") and send. The answer streams in as Corra writes it. The panel offers three starter messages while it is empty, and the buttons **New chat** and **Close**. Under each answer you can copy it, and retry the last message.

Click **Stop** to cancel an answer that is still being written.

Corra's chat is a conversation about GGX and your work in it:

- It knows what GGX is and its main concepts, such as agents, test runs, Feedback Portals, personas, prompt analysis, risk assessments and monitoring.
- It has no tools. It does not search your assets, read your data or change anything. If you ask about your own data, it can only work from what you type.
- Each message is answered on its own. Earlier messages of the same chat are not given back to the model, so repeat the context you need.

Your chats are kept under your user, so they appear in the drawer after you reload the page.

### Choose the model

Use the **Model** picker next to the message box to choose a provider and a model. The list shows models for the LLM integrations of the project you are in, or of the organization when you are not in a project. If none is set up, the picker says "No LLM models configured". Ask an administrator to add one under **Platform Settings → Integrations**.

If you do not choose, GGX uses the default model of the project. A problem with the provider, such as a wrong key or no credit left, is shown as an error in the chat.

See [Corra AI](../) for who can use Corra and how it picks a model.
