---
description: This page describes the different indexing techniques available in Pinot
---

# Indexing

Pinot supports the following indexing techniques:

* [Forward Index](forward-index.md)
  * Dictionary-encoded forward index with bit compression
  * Raw value forward index
  * Sorted forward index with run-length encoding
* [Inverted Index](inverted-index.md)
  * Bitmap inverted index
  * Sorted inverted index
* [Star-tree Index](star-tree-index.md)
* [Bloom Filter](bloom-filter.md)
* [Range Index](range-index.md)
* [Text Index](text-search-support.md)
* [Geospatial](geospatial-support.md)
* [JSON Index](json-index.md)

Each of these techniques has advantages in different query scenarios. By default, Pinot creates a dictionary-encoded forward index for each column.&#x20;

### Enabling indexes

There are 2 ways to create indexes for a Pinot table.&#x20;

#### As part of ingestion, during Pinot segment generation

Indexing is enabled by specifying the desired column names in the table config. More details about how to configure each type of index can be found in the respective index's section above or in the Table Config section.

#### Dynamically added or removed

Indexes can also be dynamically added to or removed from segments at any point. Update your table config with the latest set of indexes you wish to have.&#x20;

For example, if you have an inverted index on the `foo` field and now want to include the `bar` field, you would update your table config from this:

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

The updated index config won't be picked up unless we invoke the reload API. This API sends reload messages via Helix to all servers, as part of which indexes are added or removed from the local segments. This happens without any downtime and is completely transparent to the queries.&#x20;

When adding an index, only the new index is created and appended to the existing segment. When removing an index, its related states are cleaned up from Pinot servers. You can find this API under the `Segments` tab on Swagger:

```
curl -X POST 
"http://localhost:9000/segments/myTable/reload" 
-H "accept: application/json"
```

You can also find this action on the [Cluster Manager in the Pinot UI](https://docs.pinot.apache.org/basics/components/exploring-pinot#cluster-manager), on the specific table's page.

### Tuning Index

{% hint style="info" %}
The inverted index provides good performance for most use cases, especially if your use case doesn't have a strict low latency requirement. \
\
You should start by using this, and if your queries aren't fast enough, switch to advanced indices like the sorted or Star-Tree index.
{% endhint %}
