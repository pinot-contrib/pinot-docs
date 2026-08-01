---
description: This section contains reference documentation for the JSONPATHDOUBLE function.
---

# JSONPATHDOUBLE

Extracts the **Double** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error. This function can only be used in an [ingestion transformation function](../../build-with-pinot/ingestion/ingestion-level-transformations.md).

## Signature

> JSONPATHDOUBLE(jsonField, 'jsonPath', \[defaultValue])

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `jsonField`  | An **Identifier**/**Expression** contains JSON documents.                                              |
| `'jsonPath'` | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents. |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers**.\
\
You can use the [Jayway JsonPath Evaluator Tool](https://jsonpath.herokuapp.com/) to test JSON expressions before you import any data.
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

| Expression                      | Value  |
| ------------------------------- | ------ |
| `JSONPATHDOUBLE(data, '$.age')` | `24.0` |

This function can be used in the [table config](../../reference/configuration-reference/table.md) to extract the `age` property into the `age` column, as described below:

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

## Value conversion

`JSONPATHDOUBLE` converts a matched value to a double as follows:

| Matched value | Result |
| --- | --- |
| Number | The value's double representation |
| Boolean | `true` becomes `1.0`; `false` becomes `0.0` |
| `TIMESTAMP` in materialized input | Epoch milliseconds |
| `DATE` in materialized input | Days since the Unix epoch |
| `TIME` in materialized input | Milliseconds since midnight |

The `TIMESTAMP`, `DATE`, and `TIME` conversions apply when an extractor has already materialized the input as a record object instead of JSON text. `TIME` values drop sub-millisecond precision. Missing or null values, non-numeric values, and conversion errors return `defaultValue` when it is supplied.

## Fast and first-match variants

Use the opt-in variants below when the path is a **simple linear path**: `$` followed only by `.name`, `['literal.key']`, or `[0]` segments. For more complex JsonPath features such as wildcards, deep scan (`..`), filters, unions, slices, negative indexes, or a bare `$`, Pinot falls back to the existing `JSONPATHDOUBLE` behavior.

Like `JSONPATHDOUBLE`, both variants are intended for [ingestion transformation functions](../../build-with-pinot/ingestion/ingestion-level-transformations.md).

### JSONPATHDOUBLEFAST

> JSONPATHDOUBLEFAST(jsonField, 'jsonPath', \[defaultValue])

`JSONPATHDOUBLEFAST` resolves supported paths in a single forward pass over the JSON text instead of building the full Jayway DOM first. It keeps the same result as `JSONPATHDOUBLE`, including the same `defaultValue` handling, and falls back to the existing implementation when the path is not a simple linear path or the input is not a JSON object or array.

Use `JSONPATHDOUBLEFAST` when you want lower ingestion CPU cost without changing semantics.

### JSONPATHDOUBLEFIRSTMATCH

> JSONPATHDOUBLEFIRSTMATCH(jsonField, 'jsonPath', \[defaultValue])

`JSONPATHDOUBLEFIRSTMATCH` uses the same streaming fast path but stops as soon as the addressed field is found. This is usually the fastest option when the field appears early in the JSON document, but it changes behavior for undefined or corrupt input:

- Duplicate keys resolve to the **first** occurrence instead of the last one.
- A document malformed strictly after the addressed field can still return the extracted value.

Use `JSONPATHDOUBLEFIRSTMATCH` only when the upstream JSON is well-formed and duplicate-free.
