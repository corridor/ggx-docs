---
title: "Data Warehouses"
description: "Connect governed warehouse data to GGX for AI evaluation datasets, retrieval sources, production monitoring evidence, and lifecycle governance."
---

Data warehouses provide governed enterprise data for GGX evaluation, retrieval, monitoring, and audit workflows. Keep warehouse access controls and data policies in the warehouse, while GGX records the AI assets, test results, approvals, and findings that use the authorized data.

## Available integrations

- [Data sources](data-sources/) — Connect Snowflake, Amazon Redshift, Google BigQuery, Azure Synapse / Microsoft Fabric, PostgreSQL, MySQL / MariaDB, Oracle, MSSQL, Apache Hive, other JDBC databases, Amazon S3, Google Cloud Storage and Azure Blob, and install the Python driver each one needs.
- [Databricks](databricks-unity-catalog/) — Connect a Databricks SQL warehouse and register a table or SQL query as a GGX dataset.

For a source GGX does not list, use **Custom Logic** in [Datasets](../../register-and-refine/inventory-management/table-registry/) to write your own reader.

## Integration principles

1. Use a least-privilege identity with access only to the approved catalogs, schemas, tables, views, or volumes.
2. Prefer curated views or approved datasets over unrestricted production tables.
3. Send only the fields required for the GGX workflow; redact, tokenize, or exclude sensitive fields where appropriate.
4. Record the source, version or snapshot, owner, and refresh date in GGX so results remain reproducible.
5. Retain warehouse audit logs and GGX approval evidence according to the organization’s data-retention policy.
