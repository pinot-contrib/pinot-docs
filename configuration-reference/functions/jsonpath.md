---
description: This section contains reference documentation for the JSONPATH function.
---

# JSONPATH

Extracts the object value from jsonField based on 'jsonPath', the result type is inferred based on JSON value. This function can only be used in an [ingestion transformation function](../../developers/advanced/ingestion-level-transformations.md).

## Signature

> JSONPATH(jsonField, 'jsonPath')

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `jsonField`  | An **Identifier**/**Expression** contains JSON documents.                                              |
| `'jsonPath'` | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents. |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers.** \
\
You can use the [JsonPath tester tool](https://jsoning.com/jsonpath/) to test JSON expressions before you import any data.
{% endhint %}

## Usage Examples

The usage examples are based on extracting fields from the following JSON document:

```json
{
  "data": {
    "name": "Pete",
    "age": 24,
    "subjects": [
      {
        "name": "maths",
        "homework_grades": [80, 85, 90, 95, 100],
        "grade": "A",
        "score": 90
      },
      {
        "name": "english",
        "homework_grades": [60, 65, 70, 85, 90],
        "grade": "B",
        "score": 70
      }
    ]
  }
}
```

| Expression                 | Value    |
| -------------------------- | -------- |
| `JSONPATH(data, '$.name')` | `"Pete"` |
| `JSONPATH(data, '$.age')`  | `24`     |

This function can be used in the [table config](../table.md) to extract the `name` property into the `name` column and `age` property into the `age` column, as described below:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"name",
               "transformFunction":"JSONPATHSTRING(data, '$.name')"
            },
            {
               "columnName":"age",
               "transformFunction":"JSONPATHSTRING(data, '$.age')"
            }
         ]
      }
   }
}
```
