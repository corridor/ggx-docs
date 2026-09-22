---
title: "Databricks Unity Catalog"
description: "Use Databricks Unity Catalog-governed data assets with GGX for reproducible AI evaluation, retrieval, monitoring, and approval workflows."
---

Databricks Unity Catalog can provide governed data sources for GGX workflows. Unity Catalog remains responsible for data discovery, permissions, lineage, and audit controls; GGX uses the approved data to evaluate and monitor AI systems, then preserves the associated lifecycle evidence.

## Common patterns

- **Evaluation datasets:** Use approved Unity Catalog tables or views as GGX test datasets for simulations, comparisons, and regression testing.
- **Retrieval sources:** Build or refresh a GGX RAG knowledge source from authorized documents, tables, or volumes, with the data owner’s approval.
- **Production monitoring:** Bring selected operational records or model outcomes into GGX to run quality checks, route exceptions for review, and create findings.
- **Approval evidence:** Associate each GGX evaluation with its Unity Catalog source, snapshot or version, and access owner so reviewers can understand the evidence used.

## Recommended setup

1. Identify the Unity Catalog data asset and its accountable owner.
2. Have a Databricks administrator provide GGX with an **external use schema** and the related Unity Catalog permissions needed for the approved data assets. Scope these permissions to the catalogs, schemas, tables, views, or volumes required by the integration.
3. In GGX, configure the Databricks connection under **Org Settings > Integrations**. Enter only the connection details and credentials supplied for the dedicated GGX access path.
4. Register the dataset or retrieval source in GGX with its catalog, schema, object name, source owner, refresh schedule, and applicable data classifications. Prefer a curated view when source tables contain fields that GGX does not need.
5. Capture a stable snapshot, version, or query definition before running an evaluation. This makes a GGX result reproducible when the underlying warehouse data changes.
6. Run GGX evaluations, monitoring reports, or human review workflows against the approved data.
7. Link resulting reports, approvals, and findings back to the registered data source in GGX. Remediate data permissions and policies in Databricks; remediate AI lifecycle findings in GGX.

## Data-handling notes

- Do not copy secrets, credentials, or unrestricted personal data into GGX merely to run a test.
- Minimize the columns and rows shared with GGX, and apply masking or tokenization where the use case permits it.
- Treat source refreshes as a change to evaluation evidence. Re-run material evaluations when the source, schema, query, or data policy changes.
- Align retention and deletion requirements across both systems, especially for prompt inputs, model outputs, and reviewer annotations derived from warehouse data.
