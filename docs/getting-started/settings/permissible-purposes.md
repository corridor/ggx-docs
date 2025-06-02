# Permissible Purposes

## Overview

Permissible Purpose defines how an object can be used or where it can be used. A User can select one or multiple purpose tags to assign to the object. These tags are used to help monitor downstream functions whether the data is being used for a permissible purpose or not.

If an object is used beyond its intended permissible purpose, the system automatically tracks it and displays a "Permissible Purpose Violation" error. For example, if a model designated for Non-PII usage is applied in PII-based pipelines, the system will flag it as a violation.

## How to create Permissible Purpose?

**Permissible Purpose** registry in **Settings** shows all the registered permissible tags. The new ones can be created here:

- Click on **Create** button on **Permissible Purpose** page.
- Fill in important details like **Name** and **Description**.
- Finally click on **Create** button to register the tag.

Once registered these permissible tags can be attached to registered objects for platform to automatically govern the permissioned use in downstream application.
