# Forward Index

The values for every column are stored in a forward index, of which there are three types:

* Dictionary encoded forward index - Builds a dictionary mapping 0 indexed ids to each unique value in a column and a forward index that contains the bit-compressed ids.
* Raw value forward index - Builds a forward index of the column's values.&#x20;
* Sorted forward index - Builds a dictionary mapping from each unique value to a pair of start and end document id and a forward index on top of the dictionary encoding.

## Dictionary-encoded forward index with bit compression (default)

For each unique value from a column, we assign an id to it, and build a dictionary from the id to the value. Then in the forward index, we only store the bit-compressed ids instead of the values. With few number of unique values, dictionary-encoding can significantly improve the space efficiency of the storage.

The below diagram shows the dictionary encoding for two columns with `integer` and `string` types. As seen in the `colA`, dictionary encoding will save significant amount of space for duplicated values. On the other hand, `colB` has no duplicated data. Dictionary encoding will not compress much data in this case where there are a lot of unique values in the column. For `string` type, we pick the length of the longest value and use it as the length for dictionary’s fixed length value array. In this case, padding overhead can be high if there are a large number of unique values for a column.

![](../../.gitbook/assets/dictionary.png)

## Raw value forward index

In contrast to the dictionary-encoded forward index, raw value forward index directly stores values instead of ids.

Without the dictionary, the dictionary lookup step can be skipped for each value fetch. Also, the index can take advantage of the good locality of the values, thus improve the performance of scanning large number of values.

A typical use case to apply raw value forward index is when the column has a large number of unique values and the dictionary does not provide much compression. As seen the above diagram for dictionary encoding, scanning values with a dictionary involves a lot of random access because we need to perform dictionary look up. On the other hand, we can scan values sequentially with raw value forward index and this can improve performance a lot when applied appropriately.

![](../../.gitbook/assets/no-dictionary.png)

Raw value forward index can be configured for a table by setting it in the table config as

```javascript
{
    "tableIndexConfig": {
        "noDictionaryColumns": [
            "column_name",
            ...
        ],
        ...
    }
}
```

## Sorted forward index with run-length encoding

When a column is physically sorted, Pinot uses a sorted forward index with run-length encoding on top of the dictionary-encoding. Instead of saving dictionary ids for each document id, we store a pair of start and end document id for each value. (The below diagram does not include dictionary encoding layer for simplicity.)

![](../../.gitbook/assets/sorted-forward.png)

Sorted forward index has the advantages of both good compression and data locality. Sorted forward index can also be used as inverted index.

Sorted index can be configured for a table by setting it in the table config as

```javascript
{
    "tableIndexConfig": {
        "sortedColumn": [
            "column_name"
        ],
        ...
    }
}
```

{% hint style="info" %}
**Note**: A given Pinot table can only have 1 sorted column
{% endhint %}

Real-time server will sort data on `sortedColumn` when generating segment internally. For offline push, input data needs to be sorted before running Pinot segment conversion and push job.

When applied correctly, one can find the following information on the segment metadata.

```bash
$ grep memberId <segment_name>/v3/metadata.properties | grep isSorted
column.memberId.isSorted = true
```

##
