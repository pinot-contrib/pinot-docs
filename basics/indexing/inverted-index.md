# Inverted Index

### Bitmap inverted index

When inverted index is enabled for a column, Pinot maintains a map from each value to a bitmap, which makes value lookup to be constant time. When you have a column that is used for filtering frequently, adding an inverted index will improve the performance greatly.

Inverted index can be configured for a table by setting it in the table config as

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

### Sorted inverted index

Sorted forward index can directly be used as inverted index, with `log(n)` time lookup and it can benefit from data locality.

For the below example, if the query has a filter on `memberId`, Pinot will perform binary search on `memberId` values to find the range pair of docIds for corresponding filtering value. If the query requires to scan values for other columns after filtering, values within the range docId pair will be located together; therefore, we can benefit a lot from data locality.

![\_images/sorted-inverted.png](../../.gitbook/assets/sorted-inverted.png)

Sorted index performs much better than inverted index; however, it can only be applied to one column. When the query performance with inverted index is not good enough and most of queries have a filter on a specific column \(e.g. memberId\), sorted index can improve the query performance.

