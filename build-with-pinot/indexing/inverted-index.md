---
description: This page describes configuring the inverted index for Apache Pinot.
---

# Inverted index

The [forward index](forward-index.md) maps document IDs (rows) to values. An inverted index reverses this mapping: it maps values to the set of document IDs that contain them. When you frequently filter on a column with predicates like EQ, IN, GT, LT, or BETWEEN, adding an inverted index can significantly improve query performance.

Pinot supports two types of inverted indexes: bitmap inverted indexes and sorted inverted indexes.

## When to use

Use an inverted index on columns that appear frequently in `WHERE` clause filters, especially for equality and membership predicates. An inverted index is a good starting point for performance tuning.

- Use a **bitmap inverted index** on unsorted columns that are filtered frequently.
- Use a **sorted inverted index** (automatic when a column is sorted) when most queries filter on the same column.

## Supported column types

Bitmap inverted indexes are supported on all data types except MAP: INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL, BOOLEAN, TIMESTAMP, STRING, JSON, BYTES. Both single-value and multi-value columns are supported.

## Bitmap inverted index

When an inverted index is enabled for an unsorted column, Pinot maintains a mapping from each value to a bitmap of document IDs. This makes value lookup take constant time O(1).

### Configuration

The recommended way to enable a bitmap inverted index:

{% code title="Recommended: fieldConfigList" %}
```json
{
  "fieldConfigList": [
    {
      "name": "playerName",
      "indexes": {
        "inverted": {}
      }
    }
  ]
}
```
{% endcode %}

<details>

<summary>Older configuration</summary>

{% code title="Legacy: tableIndexConfig" %}
```json
{
  "tableIndexConfig": {
    "invertedIndexColumns": [
      "playerName"
    ]
  }
}
```
{% endcode %}

</details>

### When the index is created

> **Breaking Change (Apache Pinot PR #17951):** As of this version, the `indexingConfig.createInvertedIndexDuringSegmentGeneration` configuration flag is **no longer honored**. Inverted indexes are now **always created during segment generation** when configured, consistent with other index types. If you previously relied on deferring inverted index creation to segment loading time, this behavior has changed.

By default, bitmap inverted indexes are created during segment generation. Previously, this behavior was controlled by the table configuration option `indexingConfig.createInvertedIndexDuringSegmentGeneration` (which defaulted to `false`), but that flag is now deprecated and ignored.

## Sorted inverted index

When a column is sorted, Pinot can leverage sorted forward indexes for efficient filtering. The behavior depends on whether the column is dictionary-encoded:

**Dictionary-encoded sorted columns:** When a column is both sorted and dictionary-encoded, Pinot uses a sorted forward index with run-length encoding that also serves as an inverted index. This happens automatically and requires no extra configuration. The sorted inverted index provides `O(log n)` lookup time and benefits from data locality.

For example, if a query filters on a sorted `memberId` column, Pinot performs a binary search to find the range of document IDs matching the filter value. Subsequent column scans for those documents benefit from data locality because the matching rows are stored contiguously.

![Sorted inverted index](../../.gitbook/assets/sorted-inverted.png)

**Raw (no-dictionary) sorted columns:** As of Apache Pinot 1.3.0, raw columns can now be configured as sorted columns without forcing a dictionary or inverted index. Previously, designating a raw column as sorted would cause Pinot to force-add a dictionary and inverted index, which negated the storage benefits of raw encoding. Now, you can have sorted raw columns (for example, a timestamp column) with efficient storage while maintaining sort order metadata.

A sorted inverted index on dictionary-encoded columns offers better performance than a bitmap inverted index but can only apply to columns whose data is physically sorted within each segment. Sorted raw columns provide efficient storage for sorted data without the overhead of dictionary encoding.

## Query examples

Equality filter:

```sql
SELECT COUNT(*)
FROM baseballStats
WHERE playerName = 'Barry Bonds'
```

IN filter:

```sql
SELECT yearID, hits, homeRuns
FROM baseballStats
WHERE teamID IN ('NYA', 'BOS', 'LAD')
ORDER BY yearID
```

Filter with aggregation:

```sql
SELECT teamID, SUM(hits) AS totalHits
FROM baseballStats
WHERE league = 'NL'
GROUP BY teamID
ORDER BY totalHits DESC
LIMIT 10
```

## Limitations

- Bitmap inverted indexes require [dictionary encoding](dictionary-index.md) to be enabled on the column.
- Sorted inverted indexes (on dictionary-encoded columns) only work on columns whose data is physically sorted within each segment.
- Sorted raw columns (no-dictionary) also support sort metadata without requiring an inverted index.
- MAP columns are not supported.
