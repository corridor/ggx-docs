---
title: "Microsoft Teams"
description: "Post each new GGX issue into a Microsoft Teams channel through an Azure Bot, and keep comments, status changes, and linked tickets in the same thread."
---

[Microsoft Teams](https://www.microsoft.com/microsoft-teams) is Microsoft's team chat tool. GGX posts issues found in annotation queues and feedback portals into a Teams channel through an Azure Bot that your organization owns, and continues in the same thread. See [Issue channels](../) for what is posted.

## What it does in GGX

- Post the first message of each new issue in the channel, then reply in its thread for comments, status changes, assignment, and linked tickets.
- Update the status line of the first message when the status changes.
- Use a default channel for the organization, with an optional channel per project.
- Send messages as plain text.

## How to connect

1. In the Microsoft Entra admin center, open **App registrations** and choose **New registration**. Name it GenGuardX and choose **Accounts in this organizational directory only**. Copy the **Application (client) ID** and the **Directory (tenant) ID**.
2. Under **Certificates & secrets**, choose **New client secret** and copy its **Value** right away. Microsoft shows it once, and it expires.
3. In the Azure portal, create an **Azure Bot** resource. For **Type of App**, choose **Single Tenant** and **Use existing app registration**, with the application ID and tenant ID from step 1. The free pricing tier is enough.
4. In the bot, open **Channels** and add **Microsoft Teams**. GGX only sends messages. If Azure asks for a **Messaging endpoint**, leave it empty if the portal allows it, otherwise enter the https address of your GGX; replies sent there are ignored.
5. An administrator opens **Org Settings → Integrations → Issue trackers → Microsoft Teams** and fills in **Tenant id**, **Bot id** (the application ID), and **Client secret**, then chooses **Check connection**. **Service URL (optional)** can stay empty for the public cloud.
6. Choose **Download Teams app package**. In Teams, open **Apps**, **Manage your apps**, **Upload an app**, and add the zip to the team that owns the channel. Your Teams admin may need to allow custom apps. Add the app to every team GGX posts in.
7. In the channel, open the three dots, choose **Get link to channel**, and paste the link under **Default channel**, then choose **Use this channel**. GGX reads the team, channel, and tenant from the link, and refuses a channel from another tenant. Choose **Send test message** to confirm.

## Notes

- Only standard channels work. A bot cannot post in private or shared channels.
- GGX cannot list Teams channels, which is why you paste a link.
- A project can choose its own channel in **Project Settings → Integrations → Microsoft Teams**.
- The client secret is stored encrypted and is never shown again. It expires, so note the date and save a new one before then.
