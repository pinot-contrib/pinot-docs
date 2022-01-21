---
description: This section contains reference documentation for the JSONPATHDOUBLE function.
---

# JSONPATHDOUBLE

Extracts the <strong>Double</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.
This function can only be used in an [ingestion transformation function](../../developers/advanced/ingestion-level-transformations.md).

## Signature

> JSONPATHDOUBLE(jsonField, 'jsonPath', [defaultValue])

| Arguments  | Description                                                                                                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jsonField`      | An **Identifier**/**Expression** contains JSON documents.                                                                                                                                                                                         |
| `'jsonPath'`     | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.                                                                                                                                            |

{% hint style="warning" %}
**`'jsonPath'`**` is a literal. Pinot uses single quotes to distinguish them from **identifiers**.
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

| Expression                                                        | Value                  |
| ----------------------------------------------------------------- | ---------------------- |
| `JSONPATHDOUBLE(data, '$.age')`                           | `24.0`                 |

This function can be used in the [table config](../table.md) to extract the `age` property into the `age` column, as described below:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"age",
               "transformFunction":"JSONPATHDOUBLE(data, '$.age')"
            }
         ]
      }
   }
}
```