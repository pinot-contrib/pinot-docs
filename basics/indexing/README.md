---
description: This page describes the indexing techniques available in Apache Pinot
---

# Indexing

Apache Pinot supports the following indexing techniques:

* [Bloom filter](bloom-filter.md)
* [Forward index](forward-index.md)
  * Dictionary-encoded forward index with bit compression
  * Raw value forward index
  * Sorted forward index with run-length encoding
* [Geospatial](geospatial-support.md)
* [Inverted index](inverted-index.md)
  * Bitmap inverted index
  * Sorted inverted index
* [JSON index](json-index.md)
* [Range index](range-index.md)
* [Star-tree index](star-tree-index.md)
* Text Index
  * [Native text index](native-text-index.md)
  * [Text search support](text-search-support.md)
* [Timestamp index](timestamp-index.md)

By default, Pinot creates a dictionary-encoded forward index for each column.

### Enabling indexes

There are two ways to enable indexes for a Pinot table.

#### As part of ingestion, during Pinot segment generation

Indexing is enabled by specifying the desired column names in the table configuration. More details about how to configure each type of index can be found in the respective index's section linked above or in the [table configuration reference](../../configuration-reference/table.md).

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

You can also find this action on the [Cluster Manager in the Pinot UI](https://docs.pinot.apache.org/basics/components/exploring-pinot#cluster-manager), on the specific table's page.

{% hint style="info" %}
Not all indexes can be retrospectively applied to existing segments. For more detailed documentation on applying indexes, see the [Indexing FAQ](../getting-started/frequent-questions/ingestion-faq.md#indexing).
{% endhint %}

### Tuning Index

The inverted index provides good performance for most use cases, especially if your use case doesn't have a strict low latency requirement.

You should start by using this, and if your queries aren't fast enough, switch to advanced indices like the sorted or star-tree index.
