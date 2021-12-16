---
description: This section contains reference documentation for the JSONEXTRACTSCALAR function.
---

# JSONEXTRACTSCALAR

Evaluates the 'jsonPath' on jsonField, returns the result as the type 'resultsType', use optional defaultValuefor null or parsing error.

## Signature

> JSONEXTRACTSCALAR(jsonField, 'jsonPath', 'resultsType', [defaultValue])

| Arguments  | Description                                                                                                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jsonField`      | An **Identifier**/**Expression** contains JSON documents.                                                                                                                                                                                         |
| `'jsonPath'`     | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.                                                                                                                                            |
| `'results_type'` | <p>One of the Pinot supported data types:<strong><code>INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING,</code></strong></p><p><strong><code>INT_ARRAY, LONG_ARRAY, FLOAT_ARRAY, DOUBLE_ARRAY, STRING_ARRAY</code></strong><code>.</code></p> |

{% hint style="warning" %}
**`'jsonPath'`**` and`` `` `**`'results_type'`are literals.** Pinot uses single quotes to distinguish them from **identifiers**.
{% endhint %}

## Usage Examples

The examples in this section are based on the [Batch JSON Quick Start](../../basics/getting-started/quick-start.md#batch-json).
In particular we'll be querying the row `WHERE id = 7044874109`:

```sql
select repo
from githubEvents 
WHERE id = 7044874109
```

| repo |
| ------------- |
| {"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"} | 	

The following examples show how to use the `JSONEXTRACTSCALAR` function:

```sql
select id, jsonextractscalar(repo, '$.name', 'STRING') AS name
from githubEvents 
WHERE id = 7044874109
```

| id   | name |
| ------------- | ------------- |
| 7044874109 | 	LimeVista/Tapes  |


```sql
select id, jsonextractscalar(repo, '$.foo', 'STRING') AS name
from githubEvents 
WHERE id = 7044874109
```

```text
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

| id   | name |
| ------------- | ------------- |
| 7044874109 | 	dummyValue  |