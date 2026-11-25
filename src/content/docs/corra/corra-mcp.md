---
title: "Corra MCP settings"
description: "Use the Corra MCP page in your account settings to connect an AI client such as Claude, ChatGPT, Cursor or VS Code to GGX."
---

The **Corra MCP** page gives you the server URL and the steps to connect an AI client to GGX through the Model Context Protocol (MCP). Open it from the settings menu, under the account items next to **My Account**. Every user can open it. What a client may do is limited by your own GGX permissions. For the tools it exposes and the warnings about write actions, see [Connect GGX with MCP](/integrations/mcp/).

## Steps

1. Copy the **Server URL** with the copy button. It is your GGX address followed by `/mcp`.
2. Choose your client: **Claude**, **ChatGPT & Codex**, **Cursor**, **VS Code**, **OpenCode**, **Pi** or **Other clients**.
3. Where a client has several systems, choose one under **Where do you use it?**: Claude Code, Claude Desktop or Claude web; ChatGPT web, ChatGPT app or Codex CLI.
4. Follow the steps shown. Most end with signing in to GGX in a browser window and approving access. Commands and configuration come with a copy button and your server URL filled in.

**Other clients** uses the Streamable HTTP transport with the server URL and OAuth. No API key is needed.

## Connect with an API key

Open **Connect with an API key instead of signing in** if the sign-in is blocked. The page shows the setup with your own key in place, so copy it and restart your client.

- If you have no key yet, click **Create my API key**.
- If the key cannot be read, copy it from **My Account** and use it in place of `YOUR_API_KEY`.
- ChatGPT web and the ChatGPT app, and Claude Desktop and web, can only sign in. The page says so for those clients.

The key acts as you. Keep it private like a password.
