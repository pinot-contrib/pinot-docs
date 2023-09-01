---
description: This section contains reference documentation for the ADD function.
---

# CLPDECODE

Reconstructs (decodes) the value of a CLP-encoded field from its component columns.

The [CLPLogMessageDecoder](../../basics/data-import/clp.md) can encode fields into a set of three columns:

* `<field>_logtype`
* `<field>_dictionaryVars`
* `<field>_encodedVars`

where `<field>` is the field's name before encoding. We refer to such a set of columns as a column group.

## Signatures

> CLPDECODE(colGroupName)
> 
> CLPDECODE(colGroupName, defaultValue)
> 
> CLPDECODE(colGroupName_logtype, colGroupName_dictionaryVars, colGroupName_encodedVars)
> 
> CLPDECODE(colGroupName_logtype, colGroupName_dictionaryVars, colGroupName_encodedVars, defaultValue)

* The syntax allows you to specify just the name of a column group or all columns within the column group. 
* `defaultValue` is optional and is used when a column group can't be decoded for some reason (e.g., it's null).

## Usage Examples

Consider a record that contains a "message" field with this value:

> INFO Task task_12 assigned to container: [ContainerID:container_15], operation took 0.335 seconds. 8 tasks remaining.

[CLPLogMessageDecoder](../../basics/data-import/clp.md) will encode it into 3 columns:

| message_logtype                                                                                              | message_dictionaryVars      | message_encodedVars     |
|--------------------------------------------------------------------------------------------------------------|-----------------------------|-------------------------|
| INFO Task \x12 assigned to container: [ContainerID:\x12], operation took \x13 seconds. \x11 tasks remaining. | ["task_12", "container_15"] | [0x190000000000014f, 8] |

Then we can use `CLPDECODE` as follows:

```sql
SELECT CLPDECODE(message) AS message
FROM myTable
```

| message                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------|
| INFO Task task_12 assigned to container: [ContainerID:container_15], operation took 0.335 seconds. 8 tasks remaining. |
