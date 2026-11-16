# Hardening - Security
Source: https://docs.genguardx.ai/technology/self-hosting/hardening/
Markdown: https://docs.genguardx.ai/technology/self-hosting/hardening/index.md
Description: Harden self-hosted GGX deployments with security controls for network access, secrets, authentication, infrastructure, data storage, and operational practices.

This section describes additional setup that would be needed to make GGX secure. All the below
are recommended but optional, and can be configured as needed.

## Data Storage Security

GGX saves data in the following locations:

- Output Data Location (job results)
- File Management System
- Metadata Database
- Jupyter Content Manager (For notebooks)

Any data stored in them should be encrypted and backups should be maintained as needed.

## Network Security

The following network connections are created in GGX, and should be secured:

- **Web Application ↔︎ API Server**: HTTPS connection
- **API Server / Kernel worker ↔︎ File Management**: FTPS connection (if using FTP)
- **API Server ↔︎ Metadata Database**: SSL connections to Database
- **API Server ↔︎ Kernel worker**: Keep the kernel worker port (`5001`) reachable only from the API Server; the connection uses a token that is derived from `SECRET_KEY`
- **GGX package ↔︎ API Server**: HTTPS connection
- **Jupyter ↔︎ Web Application**: HTTPS connection
- **End User ↔︎ Web Application / Jupyter**: HTTPS / WSS connection

## Securing each component

This section describes the steps to follow for each of the GGX components to ensure it can be accessed securely.

### Common

- Ensure that all configuration and installation files are readable only by the user that the process is running with

### Web Application Server

- Ensure that the application is served using a standard web server like Nginx or Apache httpd in front of the WSGI server
- Setup the secure HTTPS protocol at the WSGI Server or the Web Server using an SSL certificate
- When setting up HTTPS, also set the JWT_COOKIE_SECURE configuration to ensure JWT cookies are sent in a secure manner
- Set a strong and unique SECRET_KEY
- It should use a reliable Authentication Provider (Avoid using the inbuilt authentication provider)

### API Server

- Ensure that the application is served using a standard web server like Nginx or Apache httpd in front of the WSGI server
- Setup the secure HTTPS protocol at the WSGI Server or the Web Server using an SSL certificate
- Set a strong and unique SECRET_KEY
- Ensure API Keys are set to ensure only authorized access to the APIs

### Kernel worker

- Ensure that only the API Server can connect to the kernel worker (by default it listens on `127.0.0.1:5001`), and use a strong and unique `SECRET_KEY`, since the worker token is derived from it.
- Kernels run as the same operating-system user as the API, so run that user without more privileges than it needs (the GGX container image runs as UID 1001 in group 0, not as root).
- Kernels only inherit the environment variables of `KERNEL_ALLOWED_ENVIRONMENT`, so the secrets of the API are not passed to them. See [Kernel Runtime](https://docs.genguardx.ai/technology/self-hosting/configurations/process-management/#kernel-runtime).

### Jupyter Notebook

- Ensure that the application is served using a standard web server like Nginx or Apache httpd in
  front of the WSGI server
- Setup the secure HTTPS protocol at the WSGI Server or the Web Server using an SSL certificate
- Ensure the standard security practices for Jupyter are followed as described in the
  [Jupyter - Security](https://jupyter.org/security) documentation.

### File Management

For Local File System: Ensure that the Hard disk being used is encrypted.

For FTP: Ensure the FTPS protocol is being used and the underlying data is encrypted

### Metadata Database (SQL RDBMS)

- Ensure that the connection to the SQL database is secured using any of the authentication methods
  available to the RDBMS.
- Ensure that the Database is encrypted.
- Ensure the standard security practices for the RDBS are followed as described in its documentation.

### Authentication Provider

- For LDAP: Ensure the secure LDAPS is used to create connections
- For SAML: Ensure a valid x509 certificate is used to authenticate messages being sent/received
