---
description: This section contains reference documentation for the JSONPATHARRAY function.
---

# JSONPATHARRAY

Extracts an array from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. This function can only be used in an [ingestion transformation function](../../developers/advanced/ingestion-level-transformations.md).

## Signature

> JSONPATHARRAY(jsonField, 'jsonPath')

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `jsonField`  | An **Identifier**/**Expression** contains JSON documents.                                              |
| `'jsonPath'` | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents. |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers**.\
\
You can use the [Jayway JsonPath Evaluator Tool](https://jsonpath.herokuapp.com/) to test JSON expressions before you import any data.&#x20;
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
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].name')`               | `["maths", "english"]` |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].score')`              | `[90, 70]`             |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].homework_grades[1]')` | `[85, 65]`             |

This function can be used in the [table config](../table.md) to extract the `name`, `score`, and second value of `homework_grades` into their respective columns , as described below:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"names",
               "transformFunction":"JSONPATHARRAY(data, '$.subjects[*].name')"
            },
            {
               "columnName":"ages",
               "transformFunction":"JSONPATHARRAY(data, '$.subjects[*].score')"
            },
            {
               "columnName":"homeworkGrades",
               "transformFunction":"JSONPATHARRAY(data, '$.subjects[*].homework_grades[1]')"
            }
         ]
      }
   }
}
```
