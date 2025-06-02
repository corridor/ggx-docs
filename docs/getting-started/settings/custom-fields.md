# Custom Fields

## Overview

The Object registries in Corridor by default, have a set of standard fields that users can fill when registering an object.The custom field capability allows users to add additional fields to the registry page.Custom fields can be created by Users with write access to the Settings module.

Based on where the values of the fields are provided - they are divided into two categories:

- **Managed within Corridor:** These Fields which are managed by users on Corridor itself
- **Managed by External System:** Allow Fields to be driven from an External System - which could be integrated via API integration or other means.

The Properties that can be assigned to a custom fields are the following:

- **Field Types**: This denotes the type of values that the custom field can take
    - Short Text: Allows users to enter any combination of letters and numbers (Value Type: Number, String)
    - Long Text: Allows users to enter up to 255 characters on separate lines
    - Single Select: Allows users to select a value from a list.
    - Fields: Options(use +/-) to add options or Enter values with each value separated by a new line
    - Multi Select: Allows users to select multiple values from a list.
    - Single File: Allows users to select a single File
    - Multiple Files: Allows users to select multiple Files
    - DateTime : Allows user to select the date and time .
- **Alias**: This the alias of the custom field (same as for other objects)
- **Default Value**: Adding a default value will auto-fill the custom field with the value when creating an object (optional)
- **Placeholder Text** : Text added in this field will be the placeholder text for that custom field (optional)
- **Help Text** : This text will show in tooltip to users understand how to use the custom field (optional)
- **Sort Order**: If there are multiple custom fields for a single object, this will be used to sort them (optional)
- **Searchable**: Checking the searchable box will allow the user to search object by using custom fields' value

## How to create a Custom Field?

- Go to **Settings** module and navigate to **Custom Field** page.
- Click on **Create** button.
- Fill in important details like **Name**, **Managed**, **Field Type**, **Field Properties**.
- Click on **Save Changes** to finally register the Custom Field.

Once created the **Custom Fields** can be organized using **Custom Screen** capability.

## Introduction to Custom Screens:

CCustom Screens enable precise configuration of Custom Field placement on the UI. Each object comes with a pre-existing Custom Screen that can be updated to include new custom fields.

## Configuring Custom Screens:

- Go to **Settings** and click on Custom Screen.
- Search the object for which custom fields needs to be added.
- Click on **Edit** button. On the right panel all the registered Custom Fields can be seen for specific object.
- One can drag all the required custom fields on the left hand side screen. Platform allows resizing, reordering etc.
- Once done with the configurations click on **Save Changes** to save the Custom Screen.

Once a Custom Screen is created, all custom fields will appear on the registry page of the corresponding object type under the "Additional Information" section. The fields will be displayed exactly as configured in the Custom Screen.

> **Note:** External Fields appear in a separate section at the end of the object's "Details" page. They cannot be edited when you edit the object in Corridor.
