# Range Index

Range indexing allows you to get better performance for queries that involve filtering over a range.

It would be useful for a query like the following:

```
SELECT COUNT(*) 
FROM baseballStats 
WHERE hits > 11
```

A range index is a variant of an [inverted index](https://docs.pinot.apache.org/basics/indexing/inverted-index), where instead of creating a mapping from values to columns, we create mapping of a range of values to columns. You can use the range index by setting the following config in the [table config](../../configuration-reference/table.md).

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

At the moment, range indexing is only supported for dictionary columns. Support for raw value columns is WIP.

{% hint style="info" %}
#### When to use Range Index?

A good thumb rule is to use a range index when you want to apply range predicates on metric columns that have a very large number of unique values.

Using an inverted index for such columns will create a very large index that is inefficient in terms of storage and performance.
{% endhint %}
