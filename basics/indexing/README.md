---
description: This page describes the different indexing techniques available in Pinot
---

# Indexing

Pinot currently supports the following indexing techniques, where each of them have their own advantages in different query scenarios.

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



By default, Pinot will use `dictionary-encoded forward index` for each column.&#x20;

### Enabling indexes

It is very easy to enable and get started with indexing in Pinot. There are 2 ways to create indexes for a Pinot table.&#x20;

#### As part of ingestion, during Pinot segment generation

Indexing is enabled by simply specifying the desired column names in the table config. More details about how to configure each type of index, can be found in the respective index's section above or in the Table Config section.

#### Dynamically added or removed

Indexes can also be dynamically added to segments or removed from segments at any point.I. Simply

Update your table config with the latest set of indexes you wish to have. For example, if you had inverted index on `foo` and now want to include `bar`, you would update your table config from this

```
"tableIndexConfig": {
        "invertedIndexColumns": ["foo"],
        ...
    }
```

to this.

```
"tableIndexConfig": {
        "invertedIndexColumns": ["foo", "bar"],
        ...
    }
```

Next, invoke reload API. This API sends reload messages via Helix to all servers, as part of which indexes are added/removed from the local segments. You can find this API under `Segments` tab on Swagger

```
curl -X POST 
"http://localhost:9000/segments/myTable/reload?forceDownload=false" 
-H "accept: application/json"
```

Or you can also find this action on the Pinot UI, on the specific table's page.



### Tuning Index

{% hint style="info" %}
If your use case is not site facing with a strict low latency requirement, the inverted index will provide good performance for most use cases. \
\
You should start by adding an inverted index and if the query does not perform as per the expectations switch to advanced indices such as sorted column and star-tree index.
{% endhint %}
