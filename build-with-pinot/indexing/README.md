---
description: Choose the Pinot index that matches your query pattern and workload.
---

# Indexing

Pinot index design is workload design. The right choice depends on whether you are optimizing point lookups, range filters, text search, JSON predicates, geospatial queries, grouping-heavy rollups, or vector similarity search.

This section helps you do three things:

1. Match a query pattern to the right index.
2. Decide whether the index belongs in the table config or can be added later.
3. Validate the choice with the query patterns you actually run.

## Start here

Use the decision guide when you know the query shape but not the best index yet.

{% content-ref url="choosing-indexes.md" %}
[choosing-indexes.md](choosing-indexes.md)
{% endcontent-ref %}

## Common index families

* [Bloom filter](bloom-filter.md) for segment pruning on highly selective lookups.
* [Forward index](forward-index.md) for Pinot's default row-to-value storage path.
* [FST index](fst-index.md) for prefix and pattern-style string filtering.
* [Inverted index](inverted-index.md) for equality, `IN`, and other highly selective filters.
* [Timestamp index](timestamp-index.md) for time-granularity queries and rollups.
* [Range index](range-index.md) for bounded numeric or time filters.
* [Text search support](text-search-support.md) for tokenized search and text predicates.
* [JSON index](json-index.md) for nested JSON predicates.
* [Geospatial support](geospatial-support.md) for distance and spatial filtering.
* [Star-tree index](star-tree-index.md) for repeatable aggregation and group-by workloads.
* [Vector index](vector-index.md) for similarity search on embeddings.

## Inspect compression efficiency

Use compression stats when you need to compare Pinot's tracked uncompressed value bytes with the bytes Pinot stores in
forward indexes and dictionaries for a table.

{% content-ref url="compression-stats.md" %}
[compression-stats.md](compression-stats.md)
{% endcontent-ref %}

### Index availability

| Index Type          | Segment Type       |
|:--------------------|:-------------------|
| Bloom filter        | Offline            |
| Forward index       | Realtime & Offline |
| FST index           | Offline            |
| Inverted index      | Realtime & Offline | 
| Timestamp index     | Offline            | 
| Sorted index        | Realtime & Offline | 
| Range index         | Offline            |
| Text search support | Realtime & Offline |
| JSON index          | Realtime & Offline |
| Geospatial support  | Realtime & Offline |
| Star-tree index     | Offline            |
| Vector index        | Realtime & Offline |

Indexes available in Realtime Segments are updated during insertion of the consumed row to the segment, so data are indexed as they become queryable.

Indexes available only in Offline segments are calculated during segment load. That means, that for offline tables indexes
become available when segment was loaded. For realtime tables, those indexes are available only for completed (not consuming) segments.

If a realtime table needs a different index layout while segments are still mutable and consuming, define
`tierOverwrites.consuming` in `tableIndexConfig` or `fieldConfigList`. Pinot applies that override only to the mutable
consuming-segment view; completed segments and immutable segment reloads continue to use the base table config.

## How Pinot applies indexes

Most index choices are defined in the table config, usually under `fieldConfigList` or `tableIndexConfig`, depending on the index and the configuration style you are using. The canonical table-level reference is [Table](../../reference/configuration-reference/table.md).

For a practical walkthrough, see [Configure indexes](../ingestion/stream-ingestion/configure-indexes.md).

Indexes can also be added or removed after ingestion for some workloads. When you need to change an existing table, prefer the current field-level configuration style over legacy index settings.

## Query patterns to keep in mind

Indexes should reflect the actual queries you run:

* `WHERE col = value` and `WHERE col IN (...)` usually want an inverted index.
* `WHERE col BETWEEN ...` or `WHERE col > ...` usually want a range-oriented strategy.
* `TEXT_MATCH(...)` wants a text index.
* `JSON_MATCH(...)` wants a JSON index.
* `ST_Distance(...)` or other spatial predicates want geospatial support.
* `GROUP BY` on a stable dimension set often benefits from star-tree.
* `VECTOR_SIMILARITY(...)` wants vector indexing.

If you are still deciding between query engines or function support, use the [Querying Pinot](../querying-and-sql/querying-pinot.md) and [SSE vs MSE](../querying-and-sql/sse-vs-mse.md) pages to confirm the query model first.

## What this page covered

This page introduced the indexing section, the main index families, and the basic rule for choosing an index from the query pattern.

## Next step

Read the decision guide to map your query pattern to a specific index and config style.

## Related pages

* [Choosing indexes](choosing-indexes.md)
* [Table](../../reference/configuration-reference/table.md)
* [Configure indexes](../ingestion/stream-ingestion/configure-indexes.md)
