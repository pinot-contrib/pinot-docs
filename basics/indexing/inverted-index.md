---
description: This page describes configuring the inverted index for Apache Pinot
---

# Inverted index

We can define the [forward index](./forward-index.md) as a mapping from document IDs (also known as rows) to values.
Similarly, an inverted index establishes a mapping from values to a set of document IDs, 
making it the "inverted" version of the forward index. 
When you frequently use a column for filtering operations like EQ (equal), IN (membership check), GT (greater than), 
etc., incorporating an inverted index can significantly enhance query performance.

Pinot supports two different inverted indexes: bitmap inverted indexes and sorted inverted indexes.
Bitmap inverted index are the _actual_ inverted index type, while the sorted type is a free index you get when the 
column is sorted.
Both type of indexes require that the [dictionary](dictionary-index.md) is enabled for the column.

Pinot supports two distinct types of inverted indexes: bitmap inverted indexes and sorted inverted indexes. 
Bitmap inverted indexes represent the _actual_ inverted index type, whereas the sorted type is automatically available 
when the column is sorted. 
Both types of indexes necessitate the enabling of a [dictionary](dictionary-index.md) for the respective column.

### Bitmap inverted index

When a column is not sorted, and an inverted index is enabled for that column, 
Pinot maintains a mapping from each value to a bitmap of rows.
This design ensures that value lookup operations take constant time, providing efficient querying capabilities.

When an inverted index is enabled for a column, Pinot maintains a map from each value to a bitmap of rows, which makes value lookup take constant time. If you have a column that is frequently used for filtering, adding an inverted index will improve performance greatly. You can create an inverted index on a multi-value column.

Inverted indexes are disabled by default and can be enabled for a column by specifying the configuration within the 
[table configuration](../../configuration-reference/table.md):

{% code title="inverted index defined in tableConfig" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "theColumnName",
      "indexes": {
        "inverted": {}
      }
    }
  ],
  ...
}
```
{% endcode %}

The older way to configure inverted indexes can also be used, although it is not actually recommended:

{% code title="old way to define inverted index in tableConfig" %}
```javascript
{
    "tableIndexConfig": {
        "invertedIndexColumns": [
            "theColumnName",
            ...
        ],
        ...
    }
}
```
{% endcode %}

#### When the index is created
By default, bitmap inverted indexes are not generated when the segment is initially created;
instead, they are created when the segment is loaded by Pinot. 
This behavior is governed by the table configuration option `indexingConfig.createInvertedIndexDuringSegmentGeneration`,
which is set to false by default.

### Sorted inverted index

As explained in the [forward index](forward-index.md) section, a column that is both sorted and equipped with a 
dictionary is encoded in a specialized manner that serves the purpose of implementing both forward and inverted indexes.
Consequently, when these conditions are met, an inverted index is effectively created without additional configuration, 
even if the configuration suggests otherwise. 
This sorted version of the forward index offers a lookup time complexity of `log(n)` and leverages data locality.

For instance, consider the following example: if a query includes a filter on the `memberId` column, Pinot will 
perform a binary search on `memberId` values to find the range pair of docIds for corresponding filtering value.
If the query needs to scan values for other columns after filtering, values within the range docId pair will be 
located together, which means we can benefit from data locality.

![\_images/sorted-inverted.png](../../.gitbook/assets/sorted-inverted.png)

A sorted inverted index indeed offers superior performance compared to a bitmap inverted index, 
but it's important to note that it can only be applied to sorted columns. 
In cases where query performance with a regular inverted index is unsatisfactory, especially when a large portion of 
queries involve filtering on the same column (e.g., `_memberId_`), using a sorted index can substantially enhance
query performance.