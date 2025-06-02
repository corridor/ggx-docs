---
title: Data Assets
---

<helper-panel object='DataTable' location='list'>

The Table Registry records the location, content, and structure of source data tables used for analytics.

The table can be registered using one of the following methods:

- **Connection to a Data Lake:** A direct link to a data lake allows specifying the location of the data file. The link must point to a valid **PySpark** data file.

- **Table Upload:** Datasets with fewer rows can be uploaded directly in CSV or Excel format.

## Managing Tables on the Platform

The **Table Registry** organizes all the registered tables into customized groups at this centralized location and allows easier tracking, monitoring, and creating new ones.

### Registering a Table:

- Click on **Create** button in Table Registry.
- Fill in important details like **Name**, and **Attributes** (Alias, Group, Input Type, Location, Description).
- Select an Input Type (Data Lake or Upload Data) and provide a data link or upload files accordingly.
- Finally, click on the **Save** button to complete the registration.

> **Note:** After registering the table, users can **Edit** and click on the **Fetch Columns** button to automatically load the table columns and their types.

Once the table is registered, data quality can be evaluated through registered **Quality Checks** or it can be used for validation and testing.

## Benefits of Table Registration:

- Automated **change history records** that tracks all the modifications to the tables.
- **Track the lineage** of table usage in downstream applications.
- Run **Quality Checks** on the tables.
- Use tables for validation and testing in a **fully auditable** manner.
- **Export tables** outside the platform when required with a single click.

</helper-panel>

<helper-panel object='QualityProfile' location='list'>

## What is a Quality Check?

The Quality Check enables the analysis of data and the creation of standard or custom reports based on registered tables in the Table Registry. It supports the generation of profiling metrics, descriptive statistics, invalid entry detection, outlier analysis, and other custom reports and metrics to assess data quality effectively before using the data for downstream tasks like running jobs.

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

</helper-panel>
