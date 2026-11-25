---
title: "Auth0 by Okta"
description: "Connect Auth0 by Okta as the SAML identity provider so users sign in to GGX with their Auth0 accounts."
---

[Auth0 by Okta](https://auth0.com/) is an identity provider. In GGX it is one of four SAML providers that share the **Configure SSO** dialog. GGX lists it with the description "SAML Integration with Auth0 by Okta".

## What it does in GGX

- Lets users sign in to GGX with their Auth0 by Okta account through the **SSO** button on the sign-in page.
- Can fill the username, email, name, title, department and project roles of a user from the attributes Auth0 by Okta sends.

## How to connect

1. In GGX, open **Org Settings → Integrations → Single Sign On (SSO)** and select **Auth0 by Okta**. The **Configure SSO** dialog opens.
2. Copy the **Entity ID** and the **Assertion Consumer Service (ACS) URL** from the dialog into the SAML application you create in Auth0 by Okta. Use Auth0 by Okta's own documentation for that step.
3. From Auth0 by Okta, copy the identity provider's entity ID, its single sign-on URL and its X.509 certificate into **Identity Provider Entity ID**, **Single Sign-On Service URL** and **X.509 Certificate Hash**.
4. Under **Attribute Mapping**, choose for **Username** and **User Email** whether GGX uses the Name ID or an attribute, and enter the attribute names Auth0 by Okta sends.
5. Optionally select **Assign Project Roles from SAML** and enter the role attribute.
6. Select **Save**.

All fields are described in [Single Sign-On (SAML)](../).

## Notes

- GGX has no Auth0 by Okta-specific fields. The dialog is the same for every SAML provider, so the exact names of the values on the Auth0 by Okta side come from Auth0 by Okta's documentation.
- For server-side settings of a self-hosted installation, see [SAML Single Sign-On](../../../technology/self-hosting/configurations/saml/).
