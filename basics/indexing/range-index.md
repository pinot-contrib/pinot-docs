---
description: This page describes configuring the range index for Apache Pinot.
---

# Range index

Range indexing allows you to get better performance for queries that involve filtering over a range.

## When to use

Use a range index when queries filter on a column with range predicates such as `>`, `<`, `>=`, `<=`, or `BETWEEN`. It is especially effective on metric columns with high cardinality, where an inverted index would be too large.

{% hint style="info" %}
A good rule of thumb is to use a range index when you want to apply range predicates on metric columns that have a very large number of unique values. Using an inverted index for such columns creates a very large index that is inefficient in terms of storage and performance.
{% endhint %}

## How it works

A range index is a variant of an [inverted index](inverted-index.md). Instead of creating a mapping from individual values to document IDs, it creates a mapping from a range of values to document IDs. At query time Pinot uses the range index to quickly identify the set of documents whose column values fall within the requested range.

## Supported column types

Range index is supported on:

- Dictionary-encoded columns of any data type (INT, LONG, FLOAT, DOUBLE, STRING, BIG_DECIMAL, BYTES, BOOLEAN, TIMESTAMP).
- Raw-encoded columns of numeric types (INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL).

{% hint style="info" %}
A range index can also be used on a dictionary-encoded time column using `STRING` type, because Pinot only supports datetime formats that are in lexicographical order.
{% endhint %}

## Configuration

The recommended way to enable a range index is through the `fieldConfigList` in the [table configuration](../../configuration-reference/table.md):

{% code title="Recommended: fieldConfigList" %}
```json
{
  "fieldConfigList": [
    {
      "name": "hits",
      "indexes": {
        "range": {}
      }
    }
  ]
}
```
{% endcode %}

You can also specify the range index version (default is `2`):

{% code title="With explicit version" %}
```json
{
  "fieldConfigList": [
    {
      "name": "hits",
      "indexes": {
        "range": {
          "version": 2
        }
      }
    }
  ]
}
```
{% endcode %}

<details>

<summary>Older configuration</summary>

The older approach uses `rangeIndexColumns` in `tableIndexConfig`:

{% code title="Legacy: tableIndexConfig" %}
```json
{
  "tableIndexConfig": {
    "rangeIndexColumns": [
      "hits"
    ]
  }
}
```
{% endcode %}

</details>

## Query examples

```sql
SELECT COUNT(*)
FROM baseballStats
WHERE hits > 11
```

```sql
SELECT playerName, hits
FROM baseballStats
WHERE hits BETWEEN 50 AND 100
ORDER BY hits DESC
LIMIT 20
```

```sql
SELECT teamID, AVG(hits) AS avgHits
FROM baseballStats
WHERE hits >= 10 AND hits <= 200
GROUP BY teamID
ORDER BY avgHits DESC
```

## Limitations

- The range index does not support MAP columns.
- When the forward index is disabled for a column, the column must be single-valued and use range index version 2 for range queries to work.
