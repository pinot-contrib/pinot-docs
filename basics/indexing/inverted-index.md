---
description: This page describes configuring the inverted index for Apache Pinot
---

# Inverted index

An inverted index stores a map of words to the documents that contain them.

## Bitmap inverted index

When an inverted index is enabled for a column, Pinot maintains a map from each value to a bitmap of rows, which makes value lookup take constant time. If you have a column that is frequently used for filtering, adding an inverted index will improve performance greatly. You can create an inverted index on a multi-value column.

An inverted index can be configured for a table by setting it in the [table configuration](../../configuration-reference/table.md):

```javascript
{
    "tableIndexConfig": {
        "invertedIndexColumns": [
            "column_name",
            ...
        ],
        ...
    }
}
```

## Sorted inverted index

A sorted forward index can directly be used as an inverted index, with `log(n)` time lookup and it can benefit from data locality.

For the following example, if the query has a filter on `memberId`, Pinot will perform a binary search on `memberId` values to find the range pair of docIds for corresponding filtering value. If the query needs to scan values for other columns after filtering, values within the range docId pair will be located together, which means we can benefit from data locality.

![\_images/sorted-inverted.png](../../.gitbook/assets/sorted-inverted.png)

A sorted index performs much better than an inverted index, but it can only be applied to one column per table. When the query performance with an inverted index is not good enough and most queries are filtering on the same column (e.g. _memberId_), a sorted index can improve the query performance.
