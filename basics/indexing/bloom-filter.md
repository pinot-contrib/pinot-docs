---
description: This page describes configuring the bloom filter for Apache Pinot
---

# Bloom filter

The bloom filter prunes segments that do not contain any record matching an **EQUALITY** predicate.

This is useful for a query like the following:

```sql
SELECT COUNT(*) 
FROM baseballStats 
WHERE playerID = 12345
```

There are 3 parameters to configure the bloom filter:

* **`fpp`**: False positive probability of the bloom filter (from `0` to `1`, `0.05` by default). The lower the `fpp` , the higher accuracy the bloom filter has, but it will also increase the size of the bloom filter.
* **`maxSizeInBytes`**: Maximum size of the bloom filter (unlimited by default). If a `fpp` setting generates a bloom filter larger than this size, using this setting will increase the `fpp` to keep the bloom filter size within this limit.
* **`loadOnHeap`**: Whether to load the bloom filter using heap memory or off-heap memory (`false` by default).

There are 2 ways to configure a bloom filter for a table in the [table configuration](../../configuration-reference/table.md):

* Default settings

```javascript
{
  "tableIndexConfig": {
    "bloomFilterColumns": [
      "playerID",
      ...
    ],
    ...
  },
  ...
}
```

* Customized parameters

```javascript
{
  "tableIndexConfig": {
    "bloomFilterConfigs": {
      "playerID": {
        "fpp": 0.01,
        "maxSizeInBytes": 1000000,
        "loadOnHeap": true
      },
      ...
    },
    ...
  },
  ...
}
```