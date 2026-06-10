---
description: This section contains reference documentation for the JSONEXTRACTOBJECT function.
---

# JSONEXTRACTOBJECT

Parses a JSON document into a reusable object or array value for downstream extraction. This function returns `null` for `null`, scalar, or non-JSON input without throwing, which makes it a good fit for [ingestion transformation functions](../../build-with-pinot/ingestion/ingestion-level-transformations.md) that need to parse once and extract many fields.

## Signature

> JSONEXTRACTOBJECT(jsonField)

| Arguments | Description |
| --- | --- |
| `jsonField` | An **Identifier** or **Expression** that contains a JSON object, JSON array, or an already-parsed container value. |

## When to use it

Use `JSONEXTRACTOBJECT` when multiple transform configs need fields from the same JSON document. Parse the document once into an intermediate column, then point `JSONPATHSTRING`, `JSONPATHLONG`, `JSONPATHDOUBLE`, or `JSONPATHARRAY` at that intermediate instead of re-parsing the original string for every extracted field.

Because the function returns `null` for plain-text or scalar input, it also works well with the default-value `JSONPATH*` overloads on columns that sometimes contain JSON and sometimes contain unstructured text.

## Usage examples

The following ingestion config parses `message` once, then extracts two fields from the parsed intermediate column:

```json
{
  "tableConfig": {
    "ingestionConfig": {
      "transformConfigs": [
        {
          "columnName": "message_obj",
          "transformFunction": "JSONEXTRACTOBJECT(message)"
        },
        {
          "columnName": "level",
          "transformFunction": "JSONPATHSTRING(message_obj, '$.level', null)"
        },
        {
          "columnName": "msg_time",
          "transformFunction": "JSONPATHSTRING(message_obj, '$.time', null)"
        }
      ]
    }
  }
}
```

When `message` is plain text instead of JSON, `JSONEXTRACTOBJECT(message)` returns `null`, so the downstream default-value extraction returns the configured default instead of failing the row.
