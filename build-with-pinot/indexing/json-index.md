---
description: This page describes configuring the JSON index for Apache Pinot.
---

# JSON index

The JSON index can be applied to JSON string columns to accelerate value lookups and filtering for the column.

## When to use JSON index

JSON strings can be used to represent arrays, maps, and nested fields without forcing a fixed schema. While JSON strings are flexible, filtering on JSON string columns is expensive, so consider the use case.

Suppose we have some JSON records similar to the following sample record stored in the `person` column:

```json
{
  "name": "adam",
  "age": 30,
  "country": "us",
  "addresses":
  [
    {
      "number" : 112,
      "street" : "main st",
      "country" : "us"
    },
    {
      "number" : 2,
      "street" : "second st",
      "country" : "us"
    },
    {
      "number" : 3,
      "street" : "third st",
      "country" : "ca"
    }
  ]
}
```

Without an index, to look up the key and filter records based on the value, Pinot must scan and reconstruct the JSON object from the JSON string for every record, look up the key and then compare the value.

For example, in order to find all persons whose name is "adam", the query will look like:

```sql
SELECT *
FROM mytable
WHERE JSON_EXTRACT_SCALAR(person, '$.name', 'STRING') = 'adam'
```

The JSON index is designed to accelerate the filtering on JSON string columns without scanning and reconstructing all the JSON objects.

## Supported column types

The JSON index is supported on STRING and MAP columns (single-valued only). It is typically used with `noDictionaryColumns` since JSON columns tend to have high cardinality.

## Enable and configure a JSON index

To enable the JSON index, you can configure the following options in the table configuration:

<table><thead><tr><th width="241">Config Key</th><th width="262">Description</th><th>Type</th><th>Default</th></tr></thead><tbody><tr><td><strong>maxLevels</strong></td><td>Max levels to flatten the json object (array is also counted as one level)</td><td>int</td><td>-1 (unlimited)</td></tr><tr><td><strong>excludeArray</strong></td><td>Whether to exclude array when flattening the object</td><td>boolean</td><td>false (include array)</td></tr><tr><td><strong>disableCrossArrayUnnest</strong></td><td>Whether to not unnest multiple arrays (unique combination of all elements in those arrays). If document contains two arrays holding, respectively M and N elements, then flattening produces M*N documents. If number of such combinations reaches 100k,  error with "Got too many combinations" message is thrown. </td><td>boolean</td><td>false (calculate unique combination of all elements)</td></tr><tr><td><strong>includePaths</strong></td><td>Only include the given paths, e.g. "<em>$.a.b</em>", "<em>$.a.c[*]</em>" (mutual exclusive with <strong>excludePaths</strong>). Paths under the included paths will be included, e.g. "<em>$.a.b.c</em>" will be included when "<em>$.a.b</em>" is configured to be included.</td><td>Set&#x3C;String></td><td>null (include all paths)</td></tr><tr><td><strong>excludePaths</strong></td><td>Exclude the given paths, e.g. "<em>$.a.b</em>", "<em>$.a.c[*]</em>" (mutual exclusive with <strong>includePaths</strong>). Paths under the excluded paths will also be excluded, e.g. "<em>$.a.b.c</em>" will be excluded when "<em>$.a.b</em>" is configured to be excluded.</td><td>Set&#x3C;String></td><td>null (include all paths)</td></tr><tr><td><strong>excludeFields</strong></td><td>Exclude the given fields, e.g. "<em>b</em>", "<em>c</em>", even if it is under the included paths.</td><td>Set&#x3C;String></td><td>null (include all fields)</td></tr><tr><td><strong>indexPaths</strong></td><td>Index the given paths, e.g. <code>*.*</code>, <code>a.**</code>. Paths matches the indexed paths will be indexed, e.g. <code>a.**</code> will index everything whose first layer is "a", <code>*.*</code> will index everything with maxLevels=2. This config could work together with other configs, e.g. includePaths, excludePaths, maxLevels but usually does not have to because it should be flexible enough to catch any scenarios.</td><td>Set&#x3C;String></td><td>null that is equivalent to <code>**</code> (include all fields)</td></tr><tr><td><strong>maxValueLength</strong></td><td>If the value of a json node (not the whole document)  is longer  than given value then replace it with <code>$SKIPPED$</code> before indexing. </td><td>int</td><td>0 (disabled)</td></tr><tr><td><strong>skipInvalidJson</strong></td><td>If set, while adding json to index, instead of throwing exception, replace ill-formed json with empty key/path and  $SKIPPED$ value .</td><td>boolean</td><td>false (disabled)</td></tr></tbody></table>

### Recommended way to configure

The recommended way to configure a JSON index is in the `fieldConfigList.indexes` object, within the `json` key.

{% code title="json index defined in tableConfig" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "person",
      "indexes": {
        "json": {
          "maxLevels": 2,
          "excludeArray": false,
          "disableCrossArrayUnnest": true,
          "includePaths": null,
          "excludePaths": null,
          "excludeFields": null,
          "indexPaths": null
        }
      }
    }
  ],
  ...
}
```
{% endcode %}

All options are optional, so the following is a valid configuration that use the default parameter values:

{% code title="json index defined in tableConfig" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "person",
      "indexes": {
        "json": {}
      }
    }
  ],
  ...
}
```
{% endcode %}

### Deprecated ways to configure JSON indexes

There are two older ways to configure the indexes that can be configured in the `tableIndexConfig` section inside table config.

The first one uses the same JSON explained above, but it is defined inside `tableIndexConfig.jsonIndexConfigs.<column name>`:

{% code title="older way to configure json indexes in table config" %}
```json
{
  "tableIndexConfig": {
    "jsonIndexConfigs": {
      "person": {
        "maxLevels": 2,
        "excludeArray": false,
        "disableCrossArrayUnnest": true,
        "includePaths": null,
        "excludePaths": null,
        "excludeFields": null,
        "indexPaths": null
      },
      ...
    },
    ...
  }
}
```
{% endcode %}

Like in the previous case, all parameters are optional, so the following is also valid:

{% code title="json index with default config" %}
```json
{
  "tableIndexConfig": {
    "jsonIndexConfigs": {
      "person": {},
      ...
    },
    ...
  }
}
```
{% endcode %}

The last option does not support to configure any parameter. In order to use this option, add the name of the column in `tableIndexConfig.jsonIndexColumns` like in this example:

{% code title="json index with default config" %}
```javascript
{
  "tableIndexConfig": {
    "jsonIndexColumns": [
      "person",
      ...
    ],
    ...
  }
}
```
{% endcode %}

#### Example:

With the following JSON document:

```json
{
  "name": "adam",
  "age": 20,
  "addresses": [
    {
      "country": "us",
      "street": "main st",
      "number": 1
    },
    {
      "country": "ca",
      "street": "second st",
      "number": 2
    }
  ],
  "skills": [
    "english",
    "programming"
  ]
}
```

Using the default setting, we will flatten the document into the following records:

```json
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1,
  "skills[1]": "programming"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "addresses[1].number": 2,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "addresses[1].number": 2,
  "skills[1]": "programming"
}
```

With **maxValueLength** set to 9:

```json
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1,
  "skills[1]": "$SKIPPED$"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "addresses[1].number": 2,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "addresses[1].number": 2,
  "skills[1]": "$SKIPPED$"
}
```

With **maxLevels** set to 1:

```json
{
  "name": "adam",
  "age": 20
}
```

With **maxLevels** set to 2:

```json
{
  "name": "adam",
  "age": 20,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "skills[1]": "programming"
}
```

With **excludeArray** set to true:

```json
{
  "name": "adam",
  "age": 20
}
```

With **disableCrossArrayUnnest** set to true:

<pre class="language-json"><code class="lang-json"><strong>{
</strong>  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1
},
{
  "name": "adam",
  "age": 20,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "skills[1]": "programming"
}
</code></pre>

When cross array un-nesting is disabled, then number of documents produced during JSON flattening is the sum of all array sizes, e.g. 2+2 = 4 in the example above.&#x20;

With **disableCrossArrayUnnest** set to false:

```json
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].number": 1,
  "addresses[0].street": "main st",
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].number": 1,
  "addresses[0].street": "main st",
  "skills[1]": "programming"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].number": 2,
  "addresses[1].street": "second st",
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].number": 2,
  "addresses[1].street": "second st",
  "skills[1]": "programming"
}
```

When cross array un-nesting is enabled, then number of documents produced during JSON flattening is the product of all array sizes, e.g. 2\*2 = 4 in the example above. If JSON contains multiple  large nested arrays, it might be necessary to disable cross array un-nesting (**disableCrossArrayUnnest=true**) to avoid hitting the 100k flattened documents limit and triggering 'Got to many combinations' error.

With **includePaths** set to \["$.name", "$.addresses\[\*].country"]:

```json
{
  "name": "adam",
  "addresses[0].country": "us"
},
{
  "name": "adam",
  "addresses[1].country": "ca"
}
```

With **excludePaths** set to \["$.age", "$.addresses\[\*].number"]:

```json
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "skills[1]": "programming"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "skills[1]": "programming"
}
```

With **excludeFields** set to \["age", "street"]:

```json
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].number": 1,
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].number": 1,
  "skills[1]": "programming"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].number": 2,
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].number": 2,
  "skills[1]": "programming"
}
```

With **indexPaths** set to \["\*", "address..country"]:

```json
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
}
```

With **skipInvalidJson** set to true, if we corrupt the original JSON, e.g. to&#x20;

```json
{ _invalid_json_
  "name": "adam",
  "age": 20,
  "addresses": [...]
  "skills": [...]
}
```

then flattening will be produce:

```json
{ "": "$SKIPPED$" }
```

Note that the JSON index can only be applied to `STRING/JSON` columns whose values are JSON strings.

{% hint style="info" %}
To reduce unnecessary storage overhead when using a JSON index, we recommend that you add the indexed column to the `noDictionaryColumns` columns list.

For instructions on that configuration property, see the [Raw value forward index](forward-index.md#raw-value-forward-index) documentation.
{% endhint %}

## How to use the JSON index

The JSON index can be used via the `JSON_MATCH` predicate for filtering: `JSON_MATCH(<column>, '<filterExpression>')`. For example, to find every entry with the name "adam":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.name"=''adam''')
```

Note that the quotes within the filter expression need to be escaped.

The JSON index can also be used via the `JSON_EXTRACT_INDEX` predicate for value extraction (optionally with filtering): `JSON_EXTRACT_INDEX(<column>, '<jsonPath>', ['resultsType'], ['filter'])`. For example, to extract every value for path `$.name` when the path `$.id` is less than 10:

```sql
SELECT jsonextractindex(repo, '$.name', 'STRING', 'dummyValue', '"$.id" < 10')
FROM mytable
```

More in-depth examples can be found in the [JSON\_EXTRACT\_INDEX function documentation](../../functions/json/jsonextractindex.md).

## Supported filter expressions

### Simple key lookup

Find all persons whose name is "adam":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.name"=''adam''')
```

or

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.name" IN (''adam'')')
```

### Chained key lookup

Find all persons who have an address (one of the addresses) with number 112:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].number"=112')
```

Find all persons who have at least one address that is not in the US:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].country" != ''us''')
```

or

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].country" NOT IN (''us'') ')
```

### Regex based lookup

Find all persons who have an address (one of the addresses) where the street contains the term 'st':

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, 'REGEXP_LIKE("$.addresses[*].street", ''.*st.*'')')
```

### Range lookup

Find all persons whose age is greater than 18:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.age" > 18')
```

Find all persons whose age is between 20 and 40 (inclusive):

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.age" BETWEEN 20 AND 40')
```

### Nested filter expression

Find all persons whose name is "adam" and also have an address (one of the addresses) with number 112:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.name"=''adam'' AND "$.addresses[*].number"=112')
```

{% hint style="info" %}
`NOT IN` and `!=` can't be used in nested filter expressions in Pinot versions older than 1.2.0. Note that `IS NULL` cannot be used in nested filter expressions currently.
{% endhint %}

### Array access

Find all persons whose first address has number 112:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[0].number"=112')
```

Since JSON index works based on flattened JSON documents, if cross array un-nesting is disabled (  **disableCrossArrayUnnest = true** ), then querying more than one array in a single JSON\_MATCH function call returns empty result, e.g.&#x20;

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].country"=''us'' AND "$.skills[*]"=''english''')
```

In such cases expression should be split into multiple JSON\_MATCH calls, e.g.

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].country"=''us''')
AND   JSON_MATCH(person, '"$.skills[*]"=''english''')
```

### Existence check

Find all persons who have a phone field within the JSON:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.phone" IS NOT NULL')
```

Find all persons whose first address does not contain floor field within the JSON:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[0].floor" IS NULL')
```

## JSON context is maintained

The JSON context is maintained for object elements within an array, meaning the filter won't cross-match different objects in the array.

To find all persons who live on "main st" in "ca":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].street"=''main st'' AND "$.addresses[*].country"=''ca''')
```

This query won't match "adam" because none of his addresses matches both the street and the country.

If you don't want JSON context, use multiple separate `JSON_MATCH` predicates. For example, to find all persons who have addresses on "main st" and have addresses in "ca" (matches need not have the same address):

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].street"=''main st''') 
  AND JSON_MATCH(person, '"$.addresses[*].country"=''ca''')
```

This query will match "adam" because one of his addresses matches the street and another one matches the country.

The array index is maintained as a separate entry within the element, so in order to query different elements within an array, multiple `JSON_MATCH` predicates are required. For example, to find all persons who have first address on "main st" and second address on "second st":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[0].street"=''main st''') 
  AND JSON_MATCH(person, '"$.addresses[1].street"=''second st''')
```

## Supported JSON values

### Object

See examples above.

### Array

```javascript
["item1", "item2", "item3"]
```

To find the records with array element "item1" in "arrayCol":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(arrayCol, '"$[*]"=''item1''')
```

To find the records with second array element "item2" in "arrayCol":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(arrayCol, '"$[1]"=''item2''')
```

### Value

```javascript
123
1.23
"Hello World"
```

To find the records with value 123 in "valueCol":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(valueCol, '"$"=123')
```

### Null

```javascript
null
```

To find the records with null in "nullableCol":

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(nullableCol, '"$" IS NULL')
```

## SELECT DISTINCT acceleration

When a JSON index is configured, you can use an index-only execution path for `SELECT DISTINCT` queries on JSON columns. Instead of scanning documents through the projection and transform pipeline, the operator reads distinct values directly from the JSON index's internal value-to-docId map, avoiding per-document evaluation entirely.

This feature is **opt-in** and must be enabled via a query option.

### How to enable

Set the `useIndexBasedDistinctOperator` query option to `true`:

```sql
SET useIndexBasedDistinctOperator = true;

SELECT DISTINCT jsonExtractIndex(person, '$.name', 'STRING')
FROM mytable
ORDER BY jsonExtractIndex(person, '$.name', 'STRING')
LIMIT 1000;
```

You can also enable it per-query via the REST API:

```
POST /query/sql
{
  "sql": "SELECT DISTINCT jsonExtractIndex(person, '$.name', 'STRING') FROM mytable",
  "queryOptions": "useIndexBasedDistinctOperator=true"
}
```

### Supported query patterns

The following table summarizes query patterns and whether they are supported by the index-based distinct operator:

| Pattern | Supported |
|---|---|
| `SELECT DISTINCT jsonExtractIndex(col, '$.path', 'STRING')` | Yes |
| `SELECT DISTINCT jsonExtractIndex(col, '$.path', 'INT')` | Yes (all single-value types) |
| `SELECT DISTINCT jsonExtractIndex(col, '$.path', 'STRING', 'default')` | Yes (with default value) |
| `SELECT DISTINCT jsonExtractIndex(col, '$.path', 'STRING', 'default', '$.filter')` | Yes (with filter JSON path) |
| With `WHERE` clause filters | Yes |
| With `ORDER BY` | Yes |
| Multi-value types (`STRING_ARRAY`, etc.) | No (falls back to default execution) |
| Multiple columns in `SELECT DISTINCT` | No (falls back to default execution) |

When a query pattern is not supported, the query still executes correctly using the default execution path.

### Prerequisites

The column must have a JSON index configured in the table config. See [Enable and configure a JSON index](#enable-and-configure-a-json-index) for configuration instructions.

The JSON path used in `jsonExtractIndex` must be included in the index. If you use `includePaths` or `indexPaths` to restrict indexed paths, ensure the path you query is covered.

### How to verify it is being used

When the index-based distinct operator is active, the query response metadata shows `numEntriesScannedPostFilter = 0` for single-server queries, because the operator reads entirely from the index without scanning any documents.

You can check this in the query response:

```json
{
  "numEntriesScannedPostFilter": 0,
  ...
}
```

If `numEntriesScannedPostFilter` is greater than zero, the query fell back to the default execution path. Verify that:

- The query option `useIndexBasedDistinctOperator` is set to `true`.
- The column has a JSON index configured.
- The query uses a supported pattern (single column, single-value type).

### Performance benefits

The index-based distinct operator avoids scanning and evaluating every document. Instead, it reads unique values directly from the JSON index structure. This provides significant performance improvements for high-cardinality JSON columns and large tables, especially when the number of distinct values is much smaller than the total number of documents.

### Limitations of SELECT DISTINCT acceleration

- The feature is disabled by default and must be enabled via the `useIndexBasedDistinctOperator` query option.
- Only single-column `SELECT DISTINCT` queries are supported. Queries with multiple columns in the `DISTINCT` clause fall back to the default execution path.
- Multi-value types (`STRING_ARRAY`, `INT_ARRAY`, etc.) are not supported and fall back to the default execution path.
- The query must use `jsonExtractIndex` (not `JSON_EXTRACT_SCALAR`) to benefit from this optimization.

## Performance Tips

### Index-Based DISTINCT Queries

If you frequently run `SELECT DISTINCT` on a JSON path that has a JSON index, enable `useIndexBasedDistinctOperator` to skip document scanning entirely:

```sql
SET useIndexBasedDistinctOperator = true;
SELECT DISTINCT jsonExtractIndex(col, '$.path', 'STRING') FROM myTable;
```

This reduces `numEntriesScannedPostFilter` to zero for qualifying queries, providing significant speedups on large tables.

## Limitations

1. The key (left-hand side) of the filter expression must be the leaf level of the JSON object, for example, `"$.addresses[*]"='main st'` won't work.
