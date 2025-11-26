---
description: This section contains reference documentation for the JSONPATHEXISTS function.
---

# JSONPATHEXISTS

Checks if specified jsonPath exists in jsonField.

## Signature

> JSONPATH(jsonField, 'jsonPath')

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `jsonField`  | An **Identifier**/**Expression** containing JSON documents.                                            |
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
| `JSONPATHEXISTS(data, '$.name')` | `true` |
| `JSONPATHEXISTS(data, '$.age')`  | `true` |
| `JSONPATHEXISTS(data, '$.shoeSize')`  | `false` |
