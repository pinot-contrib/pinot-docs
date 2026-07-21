---
description: This section contains reference documentation for the JSONPATHSTRING function.
---

# JSONPATHSTRING

Extracts the **String** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error. This function can only be used in an [ingestion transformation function](../../build-with-pinot/ingestion/ingestion-level-transformations.md).

## Signature

> JSONPATHSTRING(jsonField, 'jsonPath', \[defaultValue])

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `jsonField`  | An **Identifier**/**Expression** contains JSON documents.                                              |
| `'jsonPath'` | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents. |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers**.\
\
You can use the [JSONPath Online Evaluator](https://jsonpath.com) to test JSON expressions before you import any data.
{% endhint %}

## Usage Examples

The usage examples are based on extracting fields from the following JSON document:

```json
{
  "data": {
    "name": {"full.name": "Peter", "nick.name": "Pete"},
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

| Expression | Value |
| --- | --- |
| `JSONPATHSTRING(data, '$.age')` | `"24"` |
| `JSONPATHSTRING(data, '$.name["nick.name"]')` | "Pete" |

This function can be used in the [table config](../../reference/configuration-reference/table.md) to extract the `age` property into the `age` column, as described below:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"age",
               "transformFunction":"JSONPATHSTRING(data, '$.age')"
            },
            {
               "columnName":"nickName",
               "transformFunction":"JSONPATHSTRING(data, '$.name[\"nick.name\"]')"
            }
         ]
      }
   }
}
```

{% hint style="info" %}
When `JSONPATHSTRING` reads from an already-materialized object tree during ingestion, it preserves the extractor's runtime types instead of reparsing JSON text. For typed leaves such as `UUID`, `LocalDate`, and `LocalTime`, `JSONPATHSTRING`, `JSONPATHSTRINGFAST`, and `JSONPATHSTRINGFIRSTMATCH` now return the canonical or ISO-8601 string without JSON quotes. This compatibility change does not affect normal JSON-string input, where the parser still produces ordinary JSON scalar types.
{% endhint %}

## Fast and first-match variants

Use the opt-in variants below when the path is a **simple linear path**: `$` followed only by `.name`, `['literal.key']`, or `[0]` segments. For more complex JsonPath features such as wildcards, deep scan (`..`), filters, unions, slices, negative indexes, or a bare `$`, Pinot falls back to the existing `JSONPATHSTRING` behavior.

Like `JSONPATHSTRING`, both variants are intended for [ingestion transformation functions](../../build-with-pinot/ingestion/ingestion-level-transformations.md).

### JSONPATHSTRINGFAST

> JSONPATHSTRINGFAST(jsonField, 'jsonPath', \[defaultValue])

`JSONPATHSTRINGFAST` resolves supported paths in a single forward pass over the JSON text instead of building the full Jayway DOM first. It keeps the same result as `JSONPATHSTRING`, including the same `defaultValue` handling and the same unquoted rendering for `UUID`, `LocalDate`, and `LocalTime` leaves on already-materialized object trees, and falls back to the existing implementation when the path is not a simple linear path or the input is not a JSON object or array.

Use `JSONPATHSTRINGFAST` when you want lower ingestion CPU cost without changing semantics.

### JSONPATHSTRINGFIRSTMATCH

> JSONPATHSTRINGFIRSTMATCH(jsonField, 'jsonPath', \[defaultValue])

`JSONPATHSTRINGFIRSTMATCH` uses the same streaming fast path but stops as soon as the addressed field is found. This is usually the fastest option when the field appears early in the JSON document, but it changes behavior for undefined or corrupt input:

- Duplicate keys resolve to the **first** occurrence instead of the last one.
- A document malformed strictly after the addressed field can still return the extracted value.

Use `JSONPATHSTRINGFIRSTMATCH` only when the upstream JSON is well-formed and duplicate-free.
