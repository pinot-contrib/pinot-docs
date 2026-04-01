---
description: Pick the right Pinot index by query pattern, data shape, and workload.
---

# Choosing indexes

Use this guide when you know the query shape and need a practical recommendation.

The goal is not to enable every possible index. The goal is to keep the table config aligned with the queries that matter most.

## Decision guide

<table>
  <thead>
    <tr>
      <th>Query pattern or workload</th>
      <th>Start with</th>
      <th>Why</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Equality filters such as `WHERE userId = '...'`</td>
      <td>[Inverted index](../../basics/indexing/inverted-index.md)</td>
      <td>Fast point lookups and selective filtering.</td>
    </tr>
    <tr>
      <td>`IN` filters over a small value set</td>
      <td>[Inverted index](../../basics/indexing/inverted-index.md)</td>
      <td>Efficient membership testing within a segment.</td>
    </tr>
    <tr>
      <td>Bounded numeric or time filters</td>
      <td>[Range index](../../basics/indexing/range-index.md)</td>
      <td>Better than full scans for value intervals.</td>
    </tr>
    <tr>
      <td>Prefix, phrase, or token search</td>
      <td>[Text search support](../../basics/indexing/text-search-support.md)</td>
      <td>Designed for search-style predicates.</td>
    </tr>
    <tr>
      <td>Nested JSON predicates</td>
      <td>[JSON index](../../basics/indexing/json-index.md)</td>
      <td>Pushes JSON field filtering into the index.</td>
    </tr>
    <tr>
      <td>Distance or containment queries</td>
      <td>[Geospatial support](../../basics/indexing/geospatial-support.md)</td>
      <td>Supports spatial workloads over geographic data.</td>
    </tr>
    <tr>
      <td>Repeated `GROUP BY` and aggregate queries</td>
      <td>[Star-tree index](../../basics/indexing/star-tree-index.md)</td>
      <td>Pre-aggregates known query shapes.</td>
    </tr>
    <tr>
      <td>Embedding similarity search</td>
      <td>[Vector index](../../basics/indexing/vector-index.md)</td>
      <td>Supports approximate nearest-neighbor lookups.</td>
    </tr>
    <tr>
      <td>Stable sort-key lookups</td>
      <td>[Sorted forward index](../../basics/indexing/forward-index.md#sorted-forward-index-with-run-length-encoding)</td>
      <td>Useful when the segment sort order matches common filters.</td>
    </tr>
  </tbody>
</table>

## What to check before you configure an index

1. Verify the exact `WHERE`, `GROUP BY`, and function patterns in the query.
2. Check whether the column is dictionary encoded, single-value, multi-value, or JSON.
3. Confirm the index can be expressed in the current table config style.
4. Decide whether the index must exist on new segments only or should be reloaded onto existing segments.

For table-level configuration details, use [Table](../../configuration-reference/table.md). For an end-to-end example that applies indexes to an ingestion pipeline, use [Configure indexes](../../manage-data/data-import/pinot-stream-ingestion/configure-indexes.md).

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
* [Configure indexes](../../manage-data/data-import/pinot-stream-ingestion/configure-indexes.md)
