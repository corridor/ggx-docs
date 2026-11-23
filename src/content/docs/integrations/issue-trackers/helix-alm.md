---
title: "Perforce Helix ALM"
description: "Create and link Perforce Helix ALM issues from GGX issues on your own server, with a Helix ALM API key per person."
---

[Helix ALM](https://www.perforce.com/products/helix-alm) is Perforce's application lifecycle management tool. GGX uses it to turn issues found in annotation queues and feedback portals into Helix ALM issues.

## What it does in GGX

- Create a Helix ALM issue from a GGX issue (Issues Found), in a project you pick.
- Link an existing issue by `Project#123` or URL.
- Show each linked issue's workflow state and refresh it in the background and on demand.
- Works against your own Helix ALM server, including a private host.

## How to connect

1. GGX uses the Helix ALM REST API, which your Helix ALM administrator installs next to the server (the address looks like `https://alm.example.com/helix-alm/api/v0`). GGX must be able to reach the host, and its certificate must be one GGX trusts. A self-signed certificate is not supported.
2. An administrator saves the **Server URL** in **Org Settings → Integrations → Issue trackers → Helix ALM**.
3. A Helix ALM administrator creates an API key for each person in the Helix ALM desktop client (or the license server admin utility). The user needs a Helix ALM license, permission to log in with the REST API, and permission to add issues in the project. The secret is shown once.
4. Each person pastes the key as `key ID:secret` in **My Account → Integrations → Helix ALM**. A user name and password are not accepted.

## Notes

- Optional settings in the admin dialog: **Summary field**, **Description field** and **Status field** (the labels your projects use; they default to Summary, Description and Status), **Default text values** and **Default menu values** (JSON objects for fields your projects require; menu values must match the menu item exactly) and **Allow http** (enter `yes` only for an internal server without HTTPS; the key is then sent unencrypted).
- A workflow state named like a GGX status (Needs triage, Open, Resolved, Won't fix, Duplicate) counts as that status. Any other state is shown as written and counts as unknown.
