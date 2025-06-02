# SAML

While an internal authentication is available for simple and quick installations. It is recommended to use an enterprise-grade Identity Provider (IDP) to follow the infosec requirements for your organization. Corridor can integrate into IDPs and seamlessly be a tool in your organization.

This section describes the use of SAML (Security Assertion Markup Language) for authentication. By using SAML, it is easy to ensure that the Platform is available only to users who are authorized to use it. It makes having a centralized Identity Provider hassle-free and ensures that the standard security practices like Single Sign-On, 2-factor Authentication, etc. are consistently applied to all the organization's applications.

## Setup

To set the login based on SAML, the following information is required:

From the IDP:

- SSO URL: The URL endpoint to initiate Single Sign On requests  
  Example: `http://<idp_domain>/saml/<app_id>/sso`
- Entity ID: The URL endpoint to fetch the SAML metadata  
  Example: `http://<idp_domain>/saml/<app_id>`
- Name ID: Unique ID to identify each user
- Certificate: The X509 certificate to used to ensure any messages sent/received are trusted

From Corridor (Service Provider):

- ACS URL: `http://<sp_domain>/api/v1/saml/acs`
- Entity ID: `http://<sp_domain>/api/v1/saml/metadata`
- Start URL: `http://<sp_domain>/api/v1/users/saml/sso`

On completing the Sign On flow on the IDP side, the information returned to Corridor should contain:

- The Name ID
- The following attributes:

    - Email (The Attribute's name can be configured with `SAML_EMAIL_ATTRIBUTE`)
    - List of Roles/Groups of the user (The Attribute's name can be configured with `SAML_ROLE_ATTRIBUTE`)

### Configurations

In the API configurations, the following configurations need to be set:

- `SAML_ENABLED = True`  
  Needs to be set to enable SAML as the method of authentication for login.
- `SAML_SETTINGS = {...}`  
  Needs to be set as described in the configurations section to connect to the SP and IDP.  
  The SAML_SETTINGS is a dictionary with the following information defining the SP and IDP information:

```python
{
    # If strict is True, then the Python Toolkit will reject unsigned
    # or unencrypted messages if it expects them to be signed or encrypted.
    # Also it will reject the messages if the SAML standard is not strictly
    # followed. Destination, NameId, Conditions ... are validated too.
    "strict": true,

    # Enable debug mode (outputs errors).
    "debug": true,

    # Service Provider Data that we are deploying.
    "sp": {
        # Identifier of the SP entity  (must be a URI)
        "entityId": "https://<sp_domain>/saml/metadata/",

        # Specifies info about where and how the <AuthnResponse> message MUST be
        # returned to the requester, in this case our SP.
        "assertionConsumerService": {
            # URL Location where the <Response> from the IdP will be returned
            "url": "https://<sp_domain>/saml/acs",
            # SAML protocol binding to be used when returning the <Response>
            # message.
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
 },

        # Specifies info about where and how the <Logout Response> message MUST be
        # returned to the requester, in this case, our SP.
        "singleLogoutService": {
            # URL Location where the <Response> from the IdP will be returned
            "url": "https://<sp_domain>/saml/slo",
            # SAML protocol binding to be used when returning the <Response>
            # message.
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
 },
        # Specifies the constraints on the name identifier to be used to
        # represent the requested subject.
        "NameIDFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified",

        # The x509cert and privateKey of the SP
        'x509cert': '',
        'privateKey': ''
 },

    # Identity Provider Data that we want connected with our SP.
    "idp": {
        # Identifier of the IdP entity  (must be a URI)
        "entityId": "https://<idp_domain>/saml/metadata",

        # SSO endpoint info of the IdP. (Authentication Request protocol)
        "singleSignOnService": {
            # URL Target of the IdP where the Authentication Request Message
            # will be sent.
            "url": "https://<idp_domain>/saml/sso",
            # SAML protocol binding to be used when returning the <Response>
            # message.
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
 },

        # SLO endpoint info of the IdP.
        "singleLogoutService": {
            # URL Location of the IdP where SLO Request will be sent.
            "url": "https://<idp_domain>/saml/sls",
            # SAML protocol binding to be used when returning the <Response>
            # message.
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
 },

        # Public x509 certificate of the IdP
        "x509cert": "<connector_cert>"
        # Instead of using the whole x509cert you can use a fingerprint
        # (openssl x509 -noout -fingerprint -in "idp.crt" to generate it)
        # "certFingerprint": ""

 }
}
```
