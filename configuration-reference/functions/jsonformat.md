---
description: This section contains reference documentation for the JSONFORMAT function.
---

# JSONFORMAT

Extracts the object value from jsonField based on 'jsonPath', the result type is inferred based on JSON value. This function can only be used in an [ingestion transformation function](../../for-developers/advanced/ingestion-level-transformations.md).

## Signature

> JSONFORMAT(object)

## Usage Examples

The usage examples are based on extracting fields from the following JSON document:

```json
{"timestamp": "2019-10-09 21:25:25", "meta": {"age": 12}}
```

| Expression         | Value            |
| ------------------ | ---------------- |
| `JSONFORMAT(meta)` | `"{\"age\":12}"` |

This function can be used in the [table config](../table.md) to extract the `meta` property into the `data` column, as described below:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"data",
               "transformFunction":"JSONFORMAT(meta)"
            }
         ]
      }
   }
}
```
