---
title: "Other Git server"
description: "Clone, sync, and push Code Repos from any Git server over HTTPS or SSH, such as Gitea, Gerrit, or an in-house server."
---

Use **Other Git server** when your code is on a Git host that GGX has no dedicated integration for. It works over HTTPS or SSH, so it covers Gitea, Gerrit, Gitolite, and in-house servers.

## What it does in GGX

- Clone a repository from an allowed server into a project's **Code Repos**, then sync and push.
- Sync of these Code Repos uses the credentials of the person who cloned them.

## How an administrator sets it up

Open **Org Settings → Integrations → Source Control** and select **Other Git server**. GGX reaches only the hosts you list, so a user cannot make GGX fetch another address.

1. Under **Allowed hosts**, enter one host per line: the name and, if it is not the default, the port (443 for HTTPS, 22 for SSH). Leave it empty to turn the option off. Private addresses are fine: list them if your server is on your own network.
2. For SSH, add the server's public keys under **SSH host keys**. GGX connects only to a host whose key is listed and refuses it if the key changes. The dialog shows how to get the keys with `ssh-keyscan`. Compare the fingerprints with the ones your server administrator publishes.
3. If your HTTPS servers use a certificate from a private authority, paste it under **Private certificate authority**. GGX always verifies certificates. This adds an authority and never turns verification off.
4. Save.

GGX refuses any host that is not listed, any URL with a password in it, and any scheme except `https` and `ssh`. It always refuses link-local and cloud metadata addresses.

## How to connect and clone

1. Open **My Account → Integrations** and find **Other Git server credentials**. Pick the **Host**, then choose how you sign in:
   - HTTPS: a **Username** and a **Token or password**. The username is what your server expects with a token, such as your user name or a fixed one like `oauth2`.
   - SSH: let GGX generate an Ed25519 key, or paste a **Private key** without a passphrase. Add the public key GGX shows to your account on the server, or as a deploy key of the repository. A deploy key needs write access to push.
2. Credentials are write-only: GGX encrypts them and never shows them again. Use **Test connection** with a **Clone URL** to check that the server answers. Nothing is cloned.
3. In a project, open **Code Repos**, choose **More providers**, and select **Other Git server**. Enter the **Clone URL**, such as `https://host/team/repo.git`, `ssh://git@host/team/repo.git`, or `git@host:team/repo.git`. Do not put a password in it.
4. Give it a **Name in GGX**, optionally set a **Branch** (the server's default branch if empty), and clone.
