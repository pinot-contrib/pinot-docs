---
description: This page describes configuring the range index for Apache Pinot
---

# Range index

Range indexing allows you to get better performance for queries that involve filtering over a range.

It would be useful for a query like the following:

```sql
SELECT COUNT(*) 
FROM baseballStats 
WHERE hits > 11
```

A range index is a variant of an [inverted index](../../basics/indexing/inverted-index.md), where instead of creating a mapping from values to columns, we create mapping of a range of values to columns. You can use the range index by setting the following config in the [table configuration](../../configuration-reference/table.md).

```javascript
{
    "tableIndexConfig": {
        "rangeIndexColumns": [
            "column_name",
            ...
        ],
        ...
    }
}
```

Range index is supported for both dictionary and raw-encoded columns.

{% hint style="info" %}
A good thumb rule is to use a range index when you want to apply range predicates on metric columns that have a very large number of unique values. This is because using an inverted index for such columns will create a very large index that is inefficient in terms of storage and performance.
{% endhint %}
