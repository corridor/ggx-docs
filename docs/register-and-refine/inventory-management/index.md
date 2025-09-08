---
title: Inventory Management
---

## Overview

The platform allows registering, tracking, and monitoring of Data and GenAI assets (like RAG, Models, LLMs and Pipelines) at a centralized location.

## Why Inventory Management is Helpful?

- **Governance and Compliance:** Helps track AI models, datasets, and dependencies for regulatory audits.
- **Reusability & Efficiency**: Prevents duplication of efforts by enabling teams to reuse registered and approved assets and standardized inventories reducing onboarding time for new teams.
- **Security & Access Control**: Centralized inventories allow proper role-based access management.
- **Monitoring & Continuous Improvement**: Ensures GenAI systems can be tested before moving to production and periodically monitored post-production.

## Asset Registries:

Read more on different registries below:

- [Data Inventory](table-registry/index.md)
- [LLMs and Models](model-catalog/index.md)
- [Prompts](prompts/index.md)
- [RAGs](rags/index.md)
- [End-to-End Pipeline Assets](pipelines/index.md)

## How Platform Helps in Managing Inventories?

The platform offers extensive capabilities to streamline onboarding and efficiently manage assets.

- Multiple registries are available to centralize and manage smaller, reusable components of the pipeline.
- Customized groups for creating assets within a registry.
- Permissible Purpose Tracking that enables automatic validation to ensure components are used only for authorized purposes.
- Flexible and granular access management.
- Change History tracking for registered assets.
- Lineage Tracking of registered assets.
- Sharing of assets within and across teams.
- Creating Custom Fields for the registry apart from the default ones.

## Metadata Tagging

When any item is added to an entity - during the registration, various fields can be tagged to that object. Some basic fields are mandatory - for example:

- Alias - A Python variable name to refer to the object by
- Type - The data type that the object returns
- Description - A free format field that can be used to describe the object being created.
- Group - Useful to organize items, making them easier to search and find later
- Permissible Purpose - A governance tracking mechanism to ensure items are used correctly
- Location (of Data) - A data lake location where the data resides and can be fetched from
- Training & Validation Data - Used when creating models

New fields can be added to any of the registries to facilitate better inventory management in Settings > Fields & Screens section. Fields of various types can be added:

- Short Text
- Long Text
- Date Time
- File
- Single Select
- Multi Select
- Multiple Files

They can be marked as mandatory and customized with descriptions, placeholder values, default values, etc. and even be made mandatory to fill in. Values for fields can also be programmatically computed - with Python formulae.

### Data Type

Data Types on the platform are useful to declare clear types that can be used for documentation. Data Types are very flexible on the platform. The types supported are:

- Scalar Types:

  - Numerical
  - String
  - DateTime
  - Boolean

- Array Types:

  - Array[Numerical]
  - Array[String]
  - Array[Array[DateTime]]
  - and other types can be created by mixing existing types ...

- Struct Types:

  - Struct[decision: String, ranking: Numerical]
  - Struct[amt: Array[Numerical], flag: Boolean]
  - Struct[info: Map[Numerical,String],details: Struct[id: String,date: DateTime,age: Numerical]]
  - and other types can be created by mixing existing types ...

- Map Types:

  - Map[Numerical, String]
  - Map[String, Numerical]
  - Map[Numerical, Array[Boolean]]
  - and other types can be created by mixing existing types ...
