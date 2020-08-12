# Range Index

Range indexing allows user to get better performance for queries which involve filtering over a range. e.g.

`SELECT COUNT(*) from baseballStats where hits > 11`

Range index is just a variant of inverted index. Instead of creating mapping from values to columns, we create mapping of a range of values to columns. You can use the range index by setting the following config in the table config json.

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

Currently, range indexing is only supported for dictionary columns. Range indexing support for raw value columns is WIP.

{% hint style="info" %}
### When to use Range Index?

A good thumb rule is to use range index when you want to apply range predicates on metric columns which have very large number of unique values. Using inverted index for such columns will create a very large index that is inefficient in terms of storage and performance.
{% endhint %}

### 

### 



