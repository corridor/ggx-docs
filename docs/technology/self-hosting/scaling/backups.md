# Backups & Restore

To perform backups, it is important to understand the data that the platform uses/saves.

Data that the platform writes and the systems used for persistent storage are:

- Metadata Database
- File Management
- Data Lake
- Settings

Other than this, Redis also contains some information - but should be considered as temporary storage and not persistent.

## Backing up the systems

### Metadata Database

The entire database used for Corridor needs to be backed up.
There are 2 ways to run the backup:

- Use the standard backup manager as recommended/preferred for your RDBMS. For example: `expdp` for Oracle.
- Use the `corridor-API db export` command in Corridor to save your database into an SQLite file

The `corridor-api db export` command will create an SQLite file which is a copy of your database.
It includes various referential guarantees that databases provide like unique constraints, foreign keys, etc.
It can be directly used as an embedded database with Corridor or can be used to import back into your RDBMS of choice.
This also supports converting from 1 RBMS system to another.

### File Management

Depending on the system that is being used, backups need to be created.
If FTP or NFS is being used - the appropriate volumes/files need to be backed up.
If using a Local filesystem, the directory being used for file storage should be backed up.

### Data Lake

The path configured for `OUTPUT_DATA_LOCATION` should be backed up.
It contains various data files created by the platform.
The recommended approach to copy files for your data lake should be used.

### Settings

The instance folder of the configurations folder for Corridor should be backed up. This does not contain
any user data, and can be reconfigured later if needed.

This should be done for all the components that are running for Corridor - API, App worker, Workers, Jupyter, etc.

## Restoring the systems

### Metadata Database

The database dump from the RDBMS system can be reloaded into another database and used.

If the `corridor-api db export` method was used to create an SQLite file, the `corridor-api db import` command
can be used to import back the SQLite file into the system where the restore is being run.

### File Management

The files copied should be kept in the same structure and the user running the corridor process should have
permissions to the files on the file management system.

### Data Lake

Ideally, the data files should be copied to the same path as the original server where the backup was taken from.

### Settings

The setting files can be restored directly and permissions can be set as required.

This should be done for all the components that are running for Corridor - API, App worker, Workers, Jupyter, etc.
