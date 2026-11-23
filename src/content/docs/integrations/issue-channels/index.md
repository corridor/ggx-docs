---
title: "Issue channels"
description: "Post each new GGX issue into a Slack or Microsoft Teams channel and keep its comments, status changes, and linked tickets in the same thread."
---

An issue channel is a chat channel where GGX posts an issue from an annotation queue or feedback portal when it is created, then continues in the same thread as things happen to it. It is one-way: GGX writes to the channel and reads nothing back. A channel does not own the issue and has no ticket. For tickets, see [Issue trackers](../issue-trackers/).

| Integration | What it does |
| --- | --- |
| [Slack](slack/) | Post issues into a Slack channel with a bot token. |
| [Microsoft Teams](microsoft-teams/) | Post issues into a Teams channel with an Azure Bot. |

## What GGX posts

| Event in GGX | In the thread |
| --- | --- |
| Issue created | The first message: title, summary, status, source, number of evidence items, and a link to the issue in GGX. |
| Comment added | A reply with who commented, the comment, and a link. |
| Status changed | A reply such as "Status: Open to Resolved, by Name", and the status line of the first message is updated. |
| Assigned or unassigned | A reply in plain text. GGX does not @mention people. |
| Ticket linked or unlinked | A reply with the ticket key and its link. |

GGX does not post added or marked evidence, title edits, merges, or status changes that sync back from a linked ticket. It posts nothing retroactively: an issue created before a channel was set up is never posted.

## Where it is set up

- **Org Settings → Integrations → Issue trackers**: an administrator saves the credentials and a default channel, and can send a test message.
- **Project Settings → Integrations**: a project uses the default channel (**Use the channel of Org Settings**), picks its own, or posts nothing. The credentials always come from Org Settings.

The dialog shows delivery status for a project: whether issues are posted and where, how many posts are waiting, blocked, or given up, and the last error. **Try again** retries posts that were given up.

## Notes

- GGX does not redact anything. What a person writes in a summary or comment reaches the chat tool, with its own members and retention. GGX never sends the text of conversations.
- Posts are delivered about once a minute, in order for each issue. If the first message is deleted, GGX starts a new thread.
- If a setting must change (a revoked token, or a bot that is not in the channel), GGX marks the post as blocked and tries again every hour, so fixing the setting is enough.
