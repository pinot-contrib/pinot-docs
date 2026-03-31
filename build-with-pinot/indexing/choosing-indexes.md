---
description: Pick the right Pinot index by query pattern, data shape, and workload.
---

# Choosing indexes

Use this guide when you know the query shape and need a practical recommendation.

The goal is not to enable every possible index. The goal is to keep the table config aligned with the queries that matter most.

## Decision guide

| Query pattern or workload | Start with | Why |
| --- | --- | --- |
| Equality filters such as `WHERE userId = '...'` | [Inverted index](inverted-index.md) | Fast point lookups and selective filtering. |
| `IN` filters over a small value set | [Inverted index](inverted-index.md) | Efficient membership testing within a segment. |
| Bounded numeric or time filters | [Range index](range-index.md) | Better than full scans for value intervals. |
| Prefix, phrase, or token search | [Text search support](text-search-support.md) | Designed for search-style predicates. |
| Nested JSON predicates | [JSON index](json-index.md) | Pushes JSON field filtering into the index. |
| Distance or containment queries | [Geospatial support](geospatial-support.md) | Supports spatial workloads over geographic data. |
| Repeated `GROUP BY` and aggregate queries | [Star-tree index](star-tree-index.md) | Pre-aggregates known query shapes. |
| Embedding similarity search | [Vector index](vector-index.md) | Supports approximate nearest-neighbor lookups. |
| Stable sort-key lookups | [Sorted forward index](forward-index.md#sorted-forward-index-with-run-length-encoding) | Useful when the segment sort order matches common filters. |

## What to check before you configure an index

1. Verify the exact `WHERE`, `GROUP BY`, and function patterns in the query.
2. Check whether the column is dictionary encoded, single-value, multi-value, or JSON.
3. Confirm the index can be expressed in the current table config style.
4. Decide whether the index must exist on new segments only or should be reloaded onto existing segments.

For table-level configuration details, use [Table](../../configuration-reference/table.md). For an end-to-end example that applies indexes to an ingestion pipeline, use [Configure indexes](../ingestion/stream-ingestion/configure-indexes.md).

## Query validation examples

If you are validating an index choice, keep the query itself simple and representative.

```sql
SELECT COUNT(*)
FROM events
WHERE userId = 'u123'
```

```sql
SELECT campaign, SUM(impressions)
FROM events
WHERE eventDate BETWEEN 20240301 AND 20240331
GROUP BY campaign
```

```sql
SELECT title
FROM documents
WHERE TEXT_MATCH(title, 'pinot query engine')
```

```sql
SELECT id
FROM embeddings
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.18, 0.33], 10)
```

## Configuration style

Prefer the modern column-level configuration in `fieldConfigList` when the index supports it. Use legacy table-level settings only when you are maintaining an older table or following a migration path.

If you need to change an index on an existing table, confirm whether the change can be applied incrementally or whether the segments need to be reloaded.

## What this page covered

This page mapped common Pinot query patterns to the indexes that usually fit them best and highlighted the checks to do before changing table config.

## Next step

Open the specific index page for the workload you are tuning, then compare it with the table config and query examples for that workload.

## Related pages

* [Indexing](README.md)
* [Table](../../configuration-reference/table.md)
* [Configure indexes](../ingestion/stream-ingestion/configure-indexes.md)
