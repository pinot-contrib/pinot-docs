---
description: This section contains reference documentation for the TOJSONMAPSTR function.
---

# TOJSONMAPSTR

Convert map to JSON String.
This function can only be used in an [ingestion transformation function](../../developers/advanced/ingestion-level-transformations.md).

## Signature

> TOJSONMAPSTR(map)

## Usage Examples

The usage examples are based on extracting fields from the following JSON document:

```json
{"timestamp": "2019-10-09 21:25:25", "meta": {"age": 12}}
```

| Expression                                                        | Value                  |
| ----------------------------------------------------------------- | ---------------------- |
| `TOJSONMAPSTR(meta)`                                | `"{\"age\":12}"`               |

This function can be used in the [table config](../table.md) to extract the `meta` property into the `data` column, as described below:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"data",
               "transformFunction":"TOJSONMAPSTR(meta)"
            }
         ]
      }
   }
}
```