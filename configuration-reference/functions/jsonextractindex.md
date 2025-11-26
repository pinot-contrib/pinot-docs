---
description: >-
  This section contains reference documentation for the JSONEXTRACTINDEX function. 
---

# jsonextractindex

Evaluates the 'jsonPath' on jsonField, returns the result as the type 'resultsType', use optional defaultValuefor null or parsing error.

The function closely mirrors JSONEXTRACTSCALAR, however, since it extracts values from a JSON Index, it allows for additional filtering to be pushed down. 

Compared to JSONEXTRACTSCALAR, this is most useful when extraction is required on a large number of docs, or on large docs. When filtering is highly specific, the original JSONEXTRACTSCALAR implementation is usually faster. For a simple comparsion, see the initial PR [#11739](https://github.com/apache/pinot/pull/11739)

## Signature

> JSONEXTRACTINDEX(jsonField, 'jsonPath', 'resultsType', \[defaultValue], \[filter])

| Arguments        | Description                                                                                                                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jsonField`      | An **Identifier**/**Expression** contains JSON documents.                                                                                                                                                                                         |
| `'jsonPath'`     | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.                                                                                                                                            |
| `'resultsType'` | <p>One of the Pinot supported data types:<strong><code>INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING,</code></strong></p><p><strong><code>INT_ARRAY, LONG_ARRAY, FLOAT_ARRAY, DOUBLE_ARRAY, STRING_ARRAY</code></strong><code>.</code></p> |
| `'filter'` | <p>Pushes down a filter to avoid extracting values that do not match, e.g. <strong><code>"$.arrField[*].f2" > 2</code></strong><code>.</code></p> |

{% hint style="warning" %}
**`'jsonPath'`**` and`` `` `**`'resultsType'`are literals.** Pinot uses single quotes to distinguish them from **identifiers**.
{% endhint %}

## Usage Examples

The examples in this section are based on the [Batch JSON Quick Start](../../basics/getting-started/quick-start.md#batch-json). In particular we'll be querying the row `WHERE id = 7044874109`:

```sql
SELECT repo
from githubEvents 
WHERE id = 7044874109
```

| repo                                                                                           |
| ---------------------------------------------------------------------------------------------- |
| {"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"} |

The following examples show how to use the `JSONEXTRACTINDEX` function:

```sql
SELECT id, jsonextractindex(repo, '$.name', 'STRING') AS name
FROM githubEvents 
WHERE id = 7044874109
```

| id         | name            |
| ---------- | --------------- |
| 7044874109 | LimeVista/Tapes |


```sql
SELECT id, jsonextractindex(repo, '$.foo', 'STRING', 'dummyValue') AS name
FROM githubEvents 
WHERE id = 7044874109
```

| id         | name       |
| ---------- | ---------- |
| 7044874109 | dummyValue |

```sql
SELECT id, jsonextractindex(repo, '$.name', 'STRING', 'dummyValue', '"$.id" < 10') AS name
FROM githubEvents 
WHERE id = 7044874109
```

| id         | name            |
| ---------- | --------------- |
| 7044874109 | LimeVista/Tapes |


### Array Extraction

The below examples will use the shown arrayField

```sql
SELECT repo
FROM myTable 
WHERE id = 123
```

| repo                                                                                                |
| --------------------------------------------------------------------------------------------------- |
| {"id":"xyz"","arrayField": [{"f1": 1, "f2": 2}, {"f1": 3, "f2": 4}, {"f2": 6}, {"f1": 0, "f2": 5}]} |

Extract array values as MV 
```sql
SELECT id, jsonextractindex(repo, '$.arrayField[*].f1', 'STRING', '[]') AS arrayValues
FROM myTable 
WHERE id = 123
```

| id         | arrayValues     |
| ---------- | --------------- |
| 123        | [1, 3, 0]       |

Filtering is also allowed on array values:

```sql
SELECT id, jsonextractindex(repo, '$.arrayField[*].f1', 'STRING', '[]', '"$.arrField[*].f2" > 2') AS arrayValues
FROM myTable 
WHERE id = 123
```

| id         | arrayValues     |
| ---------- | --------------- |
| 123        | [3, 0]          |

```sql
SELECT id, jsonextractindex(repo, '$.arrayField[*].f1', 'STRING', '[]', '"$.arrField[*].nonExistant" > 99999') AS arrayValues
FROM myTable 
WHERE id = 123
```

| id         | arrayValues     |
| ---------- | --------------- |
| 123        | []              |
