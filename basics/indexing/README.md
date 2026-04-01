---
description: This page describes the indexing techniques available in Apache Pinot
---

# Indexing

Apache Pinot™ supports the following indexing techniques:

* [Bloom filter](bloom-filter.md)
* [Forward index](forward-index.md)
  * Dictionary-encoded forward index with bit compression
  * Raw value forward index
  * Sorted forward index with run-length encoding
* [FST index](fst-index.md)
* [Geospatial](geospatial-support.md)
* [Inverted index](inverted-index.md)
  * Bitmap inverted index
  * Sorted inverted index
* [JSON index](json-index.md)
* [Range index](range-index.md)
* [Star-tree index](star-tree-index.md)
* [Text search support](text-search-support.md)
* [Timestamp index](timestamp-index.md)

By default, Pinot creates a dictionary-encoded forward index for each column.

### Enabling indexes

There are two ways to enable indexes for a Pinot table.

#### As part of ingestion, during Pinot segment generation

Indexing is enabled by specifying the column names in the table configuration. More details about how to configure each type of index can be found in the respective index's section linked above or in the [table configuration reference](../../configuration-reference/table.md).

#### Dynamically added or removed

Indexes can also be dynamically added to or removed from segments at any point. Update your table configuration with the latest set of indexes you want to have.

For example, if you have an inverted index on the `foo` field and now want to also include the `bar` field, you would update your table configuration from this:

```
"tableIndexConfig": {
        "invertedIndexColumns": ["foo"],
        ...
    }
```

To this:

```
"tableIndexConfig": {
        "invertedIndexColumns": ["foo", "bar"],
        ...
    }
```

The updated index configuration won't be picked up unless you invoke the reload API. This API sends reload messages via Helix to all servers, as part of which indexes are added or removed from the local segments. This happens without any downtime and is completely transparent to the queries.

When adding an index, only the new index is created and appended to the existing segment. When removing an index, its related states are cleaned up from Pinot servers. You can find this API under the `Segments` tab on Swagger:

```
curl -X POST \
  "http://localhost:9000/segments/myTable/reload" \
  -H "accept: application/json"
```

You can also find this action on the [Cluster Manager in the Pinot UI](../components/exploring-pinot.md#cluster-manager), on the specific table's page.

{% hint style="info" %}
Not all indexes can be retrospectively applied to existing segments. For more detailed documentation on applying indexes, see the [Indexing FAQ](../../troubleshooting/ingestion-faq.md#indexing).
{% endhint %}

### Tuning Index

The inverted index provides good performance for most use cases, especially if your use case doesn't have a strict low latency requirement.

You should start by using this, and if your queries aren't fast enough, switch to advanced indices like the sorted or star-tree index.

### Data and Index types compatibility matrix

Matrix below show which combinations of data types, cardinality and encoding are compatible with various index types:

<table data-full-width="true"><thead><tr><th width="133">data type</th><th width="79">bloom</th><th width="75">fst</th><th width="75">ifst</th><th width="77">inverted</th><th width="94">geo</th><th width="98">json</th><th width="81">native</th><th width="67">text</th><th width="75">range</th><th width="94">startree</th><th width="115">timestamp</th><th width="100">vector</th></tr></thead><tbody><tr><td>boolean</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>int</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>long</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span>(2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>float</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (5)</td></tr><tr><td>double</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>big decimal</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>timestamp</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span>(2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>string</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (1)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (1)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (3)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>json</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>bytes</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="1f197">🆗</span> (2)</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr><tr><td>map</td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td><td><span data-gb-custom-inline data-tag="emoji" data-code="274c">❌</span></td></tr></tbody></table>

(1) Supports only dictionary-encoded columns.

(2) Supports only single value columns.

(3) Supported only if values can be parsed as long.

(4) Supported only if values can be parsed as json.

(5) Supports only multi value columns.

## Choosing an index

Use this decision guide to pick the right index for your query pattern:

<table>
  <thead>
    <tr>
      <th>Query pattern</th>
      <th>Recommended index</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`WHERE col = value`</td>
      <td>[Inverted index](inverted-index.md)</td>
      <td>Best starting point for equality filters</td>
    </tr>
    <tr>
      <td>`WHERE col IN (v1, v2, ...)`</td>
      <td>[Inverted index](inverted-index.md) + [Bloom filter](bloom-filter.md)</td>
      <td>Bloom filter prunes segments; inverted index accelerates within-segment lookup</td>
    </tr>
    <tr>
      <td>`WHERE col > value` / `BETWEEN`</td>
      <td>[Range index](range-index.md)</td>
      <td>Especially useful on high-cardinality metric columns</td>
    </tr>
    <tr>
      <td>`WHERE col LIKE 'prefix%'`</td>
      <td>[FST index](fst-index.md)</td>
      <td>For regex/LIKE on dictionary-encoded STRING columns</td>
    </tr>
    <tr>
      <td>`WHERE TEXT_MATCH(col, 'query')`</td>
      <td>[Text index](text-search-support.md)</td>
      <td>Full-text search with Lucene. Use for tokenized search</td>
    </tr>
    <tr>
      <td>`WHERE JSON_MATCH(col, '...')`</td>
      <td>[JSON index](json-index.md)</td>
      <td>For filtering on nested JSON fields</td>
    </tr>
    <tr>
      <td>`WHERE ST_Distance(...) < x`</td>
      <td>[Geospatial index](geospatial-support.md)</td>
      <td>H3-based spatial index for distance queries</td>
    </tr>
    <tr>
      <td>`WHERE VECTOR_SIMILARITY(...)`</td>
      <td>[Vector index](vector-index.md)</td>
      <td>Approximate nearest-neighbor search on embeddings</td>
    </tr>
    <tr>
      <td>`GROUP BY dateTrunc('DAY', ts)`</td>
      <td>[Timestamp index](timestamp-index.md)</td>
      <td>Pre-generates granularity columns for fast time-based grouping</td>
    </tr>
    <tr>
      <td>`SUM(metric) GROUP BY dim1, dim2`</td>
      <td>[Star-tree index](star-tree-index.md)</td>
      <td>Pre-aggregated results for known query patterns</td>
    </tr>
    <tr>
      <td>Sorted column, range + equality</td>
      <td>[Sorted forward index](forward-index.md#sorted-forward-index-with-run-length-encoding)</td>
      <td>Automatically acts as inverted index with O(log n) lookup</td>
    </tr>
  </tbody>
</table>
