# Data Assets
Source: https://docs.genguardx.ai/register-and-refine/inventory-management/table-registry/
Markdown: https://docs.genguardx.ai/register-and-refine/inventory-management/table-registry/index.md
Description: Register datasets from Databricks tables or SQL queries, data lakes, uploads, and custom readers, then reuse them in GGX evaluations and quality checks.

The **Datasets** page (**Data & AI Assets → Datasets**) records the location, content, and structure of source data tables used for analytics.

The table can be registered using one of the following methods:

- **Connection to a Data Lake:** A direct link to a data lake allows specifying the location of the data file. The link must point to a valid **PySpark** data file.

- **Table Upload:** Datasets with fewer rows can be uploaded directly in CSV or Excel format.

- **Databricks:** Use a configured Databricks integration to read a table by its full path or run a SQL query. See [Register a Databricks dataset](#register-a-databricks-dataset).

- **Custom Logic:** Use a custom reader for other data formats or providers supported through custom integrations.

> **Note:** Large or production-scale datasets should be registered through the **Data Lake connection** rather than uploaded through the browser. The data is then read directly from its source location (for example a cloud bucket or a PySpark/Parquet file), avoiding slow uploads while remaining viewable as a table.

## Managing Tables on the Platform

The **Datasets** page organizes all the registered tables into customized groups at this centralized location and allows easier tracking, monitoring, and creating new ones.

### Registering a Table:

- Click on **Create** button on the Datasets page.
- Fill in important details like **Name**, and **Attributes** (Alias, Group, Input Type, Location, Description).
- Select the source in **Location** and provide the data link, uploaded file, Databricks table or query, or custom read logic as appropriate.
- Finally, click on the **Save** button to complete the registration.

> **Note:** After registering the table, users can **Edit** and click on the **Fetch Columns** button to automatically load the table columns and their types.

Once the table is registered, data quality can be evaluated through registered **Quality Checks** or it can be used for validation and testing.

### Register a Databricks dataset

First, configure [Databricks under Org Settings → Integrations](https://docs.genguardx.ai/integrations/data-warehouses/databricks-unity-catalog/#connect-databricks-in-ggx). Then create a dataset and choose **Databricks** in the **Location** source selector. Use **Connect now** if the integration has not been configured.

Choose either **Table path** and enter `catalog.schema.table_name`, or **SQL query** and enter a read-only `SELECT` query. The configured Databricks SQL warehouse executes the read. Save the dataset, use **Fetch Columns** to load its schema, and check its contents through **Explore Data**.

**GGX treats Databricks as read-only and does not write to the warehouse.** Registering a dataset does not create a full copy of Databricks; GGX reads the selected table or query results for processing.

### Reuse a registered dataset

- Select it in **Data Sources** when running a [Simulation](https://docs.genguardx.ai/evaluate-and-approve/simulation/) on a Model, Prompt, RAG, or Agent.
- Use it as the shared data source for a [Comparison](https://docs.genguardx.ai/evaluate-and-approve/comparison/) between an object and its challengers.
- Link it to a [Quality Check](#what-is-a-quality-check) to profile the data and run quality reports.
- Attach evaluation jobs and reports to an [Approval Workflow](https://docs.genguardx.ai/evaluate-and-approve/approval-workflows/) as evidence for review.

## Benefits of Table Registration:

- Automated **change history records** that tracks all the modifications to the tables.
- **Track the lineage** of table usage in downstream applications.
- Run **Quality Checks** on the tables.
- Use tables for validation and testing in a **fully auditable** manner.
- **Export tables** outside the platform when required with a single click.

## What is a Quality Check?

The Quality Check enables the analysis of data and the creation of standard or custom reports based on tables registered under Datasets. It supports the generation of profiling metrics, descriptive statistics, invalid entry detection, outlier analysis, and other custom reports and metrics to assess data quality effectively before using the data for downstream tasks like running jobs.

> **Note:** The Quality Check object currently supports linking only one table at a time, enabling the generation of multiple metrics and reports for a single table per analysis.

## Managing Quality Checks on the Platform:

The **Quality Check Registry** organizes all the registered quality checks into customized groups at this centralized location and allows easier tracking, monitoring, and creating new ones.

### Registering a Quality Check:

1. Click on **Create** button in Quality Check registry.
2. Fill in important details like **Name**, **Attributes** (Data-Table, Group, Descriptions, Select Data-Columns).
3. **Add notes**, **attach documentation** if available in the **Additional Information** section.
4. Lastly, click on the **Save** button to complete the registration process.

## Benefits of Quality Check Registration:

- **Analyze and monitor data** using standard and custom reports.
- **Share data analysis and evaluations** with other team members.
