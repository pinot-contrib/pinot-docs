---
description: >-
  This section contains reference documentation for the JSONEXTRACTSCALAR
  function.
---

# jsonextractscalar

Evaluates the 'jsonPath' on jsonField, returns the result as the type 'resultsType', use optional defaultValuefor null or parsing error.

## Signature

> JSONEXTRACTSCALAR(jsonField, 'jsonPath', 'resultsType', \[defaultValue])

<table>
  <thead>
    <tr>
      <th>Arguments</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`jsonField`</td>
      <td>An **Identifier**/**Expression** contains JSON documents.</td>
    </tr>
    <tr>
      <td>`'jsonPath'`</td>
      <td>Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.</td>
    </tr>
    <tr>
      <td>`'resultsType'`</td>
      <td><p>One of the Pinot supported data types:<strong><code>INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING,</code></strong></p><p><strong><code>INT_ARRAY, LONG_ARRAY, FLOAT_ARRAY, DOUBLE_ARRAY, STRING_ARRAY</code></strong><code>.</code></p></td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>repo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"}</td>
    </tr>
  </tbody>
</table>

The following examples show how to use the `JSONEXTRACTSCALAR` function:

```sql
select id, jsonextractscalar(repo, '$.name', 'STRING') AS name
from githubEvents 
WHERE id = 7044874109
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>LimeVista/Tapes</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>dummyValue</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>missingField</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>(null)</td>
    </tr>
  </tbody>
</table>

Without null handling or when using a non-null default value, the function behaves as before, returning the specified default value or string `"null"`.
