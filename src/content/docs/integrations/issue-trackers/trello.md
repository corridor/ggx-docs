---
title: "Trello"
description: "Create and link Trello cards from GGX issues, with a Power-Up API key saved once by an administrator and a Trello token per person."
---

[Trello](https://trello.com/) is a board-based project tracker. GGX uses it to turn issues found in annotation queues and feedback portals into Trello cards.

## What it does in GGX

- Create a card from a GGX issue (Issues Found), in a board and list you pick.
- Link an existing card by URL.
- Show each linked card's status and refresh it in the background and on demand.
- Cards are created as the person who connected.

## How to connect

1. An administrator creates a Power-Up for the Workspace on the Trello Power-Ups admin page (`trello.com/power-ups/admin`), generates an API key on its **API key** tab, and adds the allowed origin that GGX shows. They save the **API key** in **Org Settings → Integrations → Issue trackers → Trello**, with an optional **App name** that Trello shows to people (GenGuardX when empty). The secret is not needed.
2. Each person opens **My Account → Integrations → Trello**, opens the link there to allow access in Trello, and pastes the token Trello shows.

## Notes

- A Trello card has no status. The list a card is in is its status. On every board that gets tickets, create lists named Needs triage, Open, Resolved, Won't fix and Duplicate. A list with another name counts as unknown, and an archived card counts as Resolved.
- Removing the API key stops everyone's saved tokens from working until an administrator saves a key again.
