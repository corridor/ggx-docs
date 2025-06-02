---
title: Global Functions
---

<helper-panel object='Global Function' location='list'>

## What are Global Functions?

Global function gives the ability to execute a set of analytical operations multiple times using different objects as inputs without having to rewrite those operations every time. It supports inputs and outputs of any type, including DataFrames, dictionaries, and other standard Python data types, without mandatorily requiring predefined input-output formats.

Global Function can be used across the platform in GenAI Studio, Reports, Simulation Data-Sources, or even within other Global Functions, offering enhanced reusability.

## Maintaining Global Functions on the Platform:

The **Global Function** registry organizes all the registered utilities into customized groups at this centralized location, allowing easier tracking, monitoring, and new function creation.

### Global Function Registration:

1. Click on **Create** button in Global function registry.
2. Fill in important details like **Name**, **Attribute** (Output Type, Alias), **Properties** (Description, Group, Approval Workflow).
3. **Define Input Arguments** along with their types and default values.
4. **Select other global functions** if required in Inputs section to help in writing logic.
5. **Write code logic** in definition source.
6. **Add notes**, **attach documentation** if available in the **Additional Information** section.
7. Click on **Save** button to finally register the function.

> **Note:** Output type is not mandatory for function registry. If missing platform allows returning any type including dataframes, dictionaries etc.

Once registration is completed, the Global Functions can be used all across the platform in GenAI Studio, Report Writing, etc.

## Benefits of Global Functions Registration:

- **Enhances reusability** across downstream applications and enables usage tracking with **Lineage Tracking**.
- Automated tracking and **recording of modifications** with efficient version upgrades.
- **Better collaboration** for continuous model building and testing.
- **Full auditability** and approvals for future usages.

</helper-panel>
