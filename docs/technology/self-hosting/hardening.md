---
title: Hardening - Security
---

This section describes additional setup that would be needed to make Corridor secure. All the below
are recommended but optional, and can be configured as needed.

## Data Storage Security

Corridor saves data in the following locations:

- Data Lake
- File Management System
- Metadata Database
- Redis (only short-term storage)
- Jupyter Content Manager (For notebooks)

Any data stored in them should be encrypted and backups should be maintained as needed.

## Network Security

The following network connections are created in Corridor, and should be secured:

- **Web Application ↔︎ API Server**: HTTPS connection
- **API Server / API - Celery ↔︎ File Management**: FTPS connection (if using FTP)
- **API Server / API - Celery ↔︎ Metadata Database**: SSL connections to Database
- **API Server / API - Celery / Spark - Celery ↔︎ Redis**: TLS authenticated Redis connection
- **Spark - Celery / Jupyter ↔︎ Spark**: Kerberos
- **Corridor Package ↔︎ API Server**: HTTPS connection
- **Jupyter ↔︎ Web Application**: HTTPS connection
- **End User ↔︎ Web Application / Jupyter**: HTTPS / WSS connection

## Securing each component

This section describes the steps to follow for each of the Corridor components to ensure it can be accessed securely.

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

### API - Celery worker

No specific steps are required for the API - Celery workers as no other component connects to it directly.

### Spark - Celery worker

- Ensure that the cluster is Kerberized
- Ensure the standard security practices for Spark are followed as described in the
  [Spark - Security](https://spark.apache.org/docs/latest/security.html) documentation.

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

### Messaging Queue (Redis)

For Redis:

- Use a secure protocol like TLS (if using Redis) when accessing the queue
- Limit the incoming connections by whitelisting the IPs of the Redis clients
- Enable the authentication feature in Redis is enabled
- Ensure the standard security practices for Redis are followed as described in the
  [Redis - Security](https://redis.io/topics/security) documentation.

### Authentication Provider

- For LDAP: Ensure the secure LDAPS is used to create connections
- For SAML: Ensure a valid x509 certificate is used to authenticate messages being sent/received
