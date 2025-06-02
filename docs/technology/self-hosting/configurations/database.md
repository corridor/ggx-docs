# Metadata: Database Setup

This section describes the different database options available for the Metadata Database. Choosing
the right database is critical, as it will impact the usability of the API and Web Application of
the users. The metadata database stores all the information entered into the Web Application in a
structured so it can be efficiently used by other components.

The platform currently supports the following databases:

- Oracle Database - Industry-standard
- SQLite - Meant for testing only
- MS SQL - Enterprise-level solution
- PostgreSQL - Open-source and reliable

# POSTGRESQL

To use postgresql, use the following configurations:

    SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@<hostname>/<dbname>'

# SQLite

Supported versions: sqlite 3+

Sqlite is an easy to setup database which is file-based. To use sqlite with Corridor, set the following configuration:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///<filepath>

# Oracle DB

Supported versions: Oracle DB 19+

To use oracle, use the following configurations:

    SQLALCHEMY_DATABASE_URI = 'oracle://<username>:<password>@<hostname>/<dbname>'

# MS SQL

Supported versions: SQL Server 2016+

This required the the unixODBC devel libraries (`yum install unixODBC-devel`) and [SQL Server ODBC driver](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server) to be installed.

To use mssql, use the following configurations:

    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://<username>:<password>@<hostname>/<dbname>?driver=ODBC+Driver+17+for+SQL+Server'
