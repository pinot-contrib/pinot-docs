---
description: >-
  This section contains reference documentation for the JSONEXTRACTSCALAR
  function.
---

# jsonextractscalar

Evaluates `'jsonPath'` on `jsonField` and coerces the resolved value to the requested `'resultsType'`. Use the optional `defaultValue` when missing paths, nulls, or parsing failures should not fail the query.

## Signature

> JSONEXTRACTSCALAR(jsonField, 'jsonPath', 'resultsType', \[defaultValue])

| Arguments       | Description                                                                                                                                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jsonField`     | An **Identifier**/**Expression** that contains JSON documents.                                                                                                                                                                                    |
| `'jsonPath'`    | Follows [JsonPath syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.                                                                                                                                            |
| `'resultsType'` | A supported Pinot result type. Common query-facing types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `BOOLEAN`, `TIMESTAMP`, and `STRING`. Append `_ARRAY` for multi-value results such as `INT_ARRAY`, `STRING_ARRAY`, or `BIG_DECIMAL_ARRAY`. |

{% hint style="warning" %}
**`'jsonPath'`**` and`` `` `**`'resultsType'`are literals.** Pinot uses single quotes to distinguish them from **identifiers**.
{% endhint %}

## Usage Examples

The examples in this section are based on the [Batch JSON Quick Start](../../basics/getting-started/quick-start.md#batch-json). In particular we'll be querying the row `WHERE id = 7044874109`:

```sql
select repo
from githubEvents 
WHERE id = 7044874109
```

| repo                                                                                           |
| ---------------------------------------------------------------------------------------------- |
| {"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"} |

The following examples show how to use the `JSONEXTRACTSCALAR` function:

```sql
select id, jsonextractscalar(repo, '$.name', 'STRING') AS name
from githubEvents 
WHERE id = 7044874109
```

| id         | name            |
| ---------- | --------------- |
| 7044874109 | LimeVista/Tapes |

```sql
select id, jsonextractscalar(repo, '$.foo', 'STRING') AS name
from githubEvents 
WHERE id = 7044874109
```

```
[
  {
    "message": "QueryExecutionError:\njava.lang.RuntimeException: Illegal Json Path: [$.foo], when reading [{\"id\":115911530,\"name\":\"LimeVista/Tapes\",\"url\":\"https://api.github.com/repos/LimeVista/Tapes\"}]\n\tat org.apache.pinot.core.operator.transform.function.JsonExtractScalarTransformFunction.transformToStringValuesSV(JsonExtractScalarTransformFunction.java:254)\n\tat org.apache.pinot.core.operator.docvalsets.TransformBlockValSet.getStringValuesSV(TransformBlockValSet.java:90)\n\tat org.apache.pinot.core.common.RowBasedBlockValueFetcher.createFetcher(RowBasedBlockValueFetcher.java:64)\n\tat org.apache.pinot.core.common.RowBasedBlockValueFetcher.<init>(RowBasedBlockValueFetcher.java:32)",
    "errorCode": 200
  }
]
```

```sql
select id, jsonextractscalar(repo, '$.foo', 'STRING', 'dummyValue') AS name
from githubEvents 
WHERE id = 7044874109
```

| id         | name       |
| ---------- | ---------- |
| 7044874109 | dummyValue |

## Result typing and coercion

`JSONEXTRACTSCALAR` now documents the per-value coercion rules that Pinot applies after resolving the JsonPath. These are the user-facing behaviors to rely on when you pick a `resultsType`:

- `BIG_DECIMAL` and `BIG_DECIMAL_ARRAY` preserve JSON numeric precision instead of round-tripping through `DOUBLE`. Use these result types when the JSON payload can contain high-precision decimal values.
- `STRING` and `STRING_ARRAY` return JSON strings as-is. For numbers, booleans, arrays, and objects, Pinot serializes the resolved JSON value back to compact JSON text.
- Numeric result types coerce each resolved value independently. This means arrays such as `[1, "2", true]` can be read as `INT_ARRAY`, and Pinot converts the elements to `1`, `2`, and `1`.
- `BOOLEAN` and `BOOLEAN_ARRAY` follow Pinot's boolean coercion rules: non-zero numbers are `true`, zero is `false`, and strings such as `"true"` or `"1"` are also treated as `true`.
- `TIMESTAMP` and `TIMESTAMP_ARRAY` accept epoch milliseconds as numbers or strings, and also accept ISO-8601 timestamp strings.

For example, these queries are now safe and source-backed:

```sql
select jsonextractscalar(payload, '$.prices', 'BIG_DECIMAL_ARRAY') as prices
from myTable
```

Use `BIG_DECIMAL_ARRAY` when values such as `12345678901234567890.123456789` must keep their exact decimal precision.

```sql
select jsonextractscalar(payload, '$.metadata', 'STRING') as metadata_json
from myTable
```

If `$.metadata` resolves to a JSON object or array, Pinot returns compact JSON text such as `{"a":1}` or `[1,2,3]` instead of failing a runtime cast.

## Null Handling

When Pinot's null handling is enabled (via `SET enableNullHandling = true`), the behavior of `JSONEXTRACTSCALAR` with a `'null'` default value has been enhanced:

- If the default value parameter is explicitly set to `'null'` and null handling is enabled, `jsonextractscalar` now correctly returns a SQL NULL instead of the string `"null"` for missing JSON paths or null values.
- This allows for proper propagation of SQL NULLs in query results, improving null semantics and consistency.

### Example with Null Handling

```sql
SET enableNullHandling = true;

select id, jsonextractscalar(repo, '$.missingPath', 'STRING', 'null') AS missingField
from githubEvents 
WHERE id = 7044874109
```

With null handling enabled, the result will be SQL NULL (empty/null in the result set) rather than the string `"null"`:

| id         | missingField |
| ---------- | ------------ |
| 7044874109 | (null)       |

Without null handling or when using a non-null default value, the function behaves as before, returning the specified default value or string `"null"`.
