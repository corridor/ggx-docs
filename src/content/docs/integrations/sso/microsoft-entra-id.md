---
title: "Microsoft Entra ID"
description: "Connect Microsoft Entra ID as the SAML identity provider so users sign in to GGX with their Microsoft accounts."
---

[Microsoft Entra ID](https://entra.microsoft.com/) is an identity provider. In GGX it is one of four SAML providers that share the **Configure SSO** dialog. GGX lists it with the description "Integrate with Microsoft Entra ID (formerly Azure Active Directory)".

## What it does in GGX

- Lets users sign in to GGX with their Microsoft Entra ID account through the **SSO** button on the sign-in page.
- Can fill the username, email, name, title, department and project roles of a user from the attributes Microsoft Entra ID sends.

## How to connect

1. In GGX, open **Org Settings → Integrations → Single Sign On (SSO)** and select **Microsoft Entra ID**. The **Configure SSO** dialog opens.
2. Copy the **Entity ID** and the **Assertion Consumer Service (ACS) URL** from the dialog into the SAML application you create in Microsoft Entra ID. Use Microsoft Entra ID's own documentation for that step.
3. From Microsoft Entra ID, copy the identity provider's entity ID, its single sign-on URL and its X.509 certificate into **Identity Provider Entity ID**, **Single Sign-On Service URL** and **X.509 Certificate Hash**.
4. Under **Attribute Mapping**, choose for **Username** and **User Email** whether GGX uses the Name ID or an attribute, and enter the attribute names Microsoft Entra ID sends.
5. Optionally select **Assign Project Roles from SAML** and enter the role attribute.
6. Select **Save**.

All fields are described in [Single Sign-On (SAML)](../).

## Notes

- GGX has no Microsoft Entra ID-specific fields. The dialog is the same for every SAML provider, so the exact names of the values on the Microsoft Entra ID side come from Microsoft Entra ID's documentation.
- For server-side settings of a self-hosted installation, see [SAML Single Sign-On](../../../technology/self-hosting/configurations/saml/).
