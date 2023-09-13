# Forward index

At conceptual level, the forward index is a map from the document ID (aka row index) to the actual column value of the row.
How this map is implemented depends on the index encoding and on whether the column is sorted or not.

When encoding is `RAW`, the forward index is implemented as an array whose indexes are the document IDs and the values
are the actual row value. 
To learn more, see the [raw value forward type](forward-index.md#raw-value-forward-index).

When the encoding is `DICTIONARY`, the forward index does not physically store the actual row values but the dictionary IDs.
This means that there is an extra indirection each time a value has to be read, but enable two more efficient physical 
layouts depending on whether the segment is sorted by this column or not.
The [dictionary encoded forward index](forward-index.md#dictionary-encoded-forward-index-with-bit-compression-default) 
and [sorted forward index](forward-index.md#sorted-forward-index-with-run-length-encoding) explain each option in detail.

## Configuration

Forward indexes are enabled by default.
This means that columns will contain a forward index unless they are explicitly disabled.
By doing so, most scanning access to the data will be disabled, but this is useful when other indexes are sufficient to cover the required data patterns.
For examples, see [Disabling the forward index](forward-index.md#disabling-the-forward-index) .

The encoding and whether the segment is sorted by the indexed column are two important properties.
They can be configured in [table config](../../configuration-reference/table.md).

When encoding is raw, forward indexes can be customized further. For more information, see the [raw encoding section](forward-index.md#raw-value-forward-index).

## Dictionary-encoded forward index with bit compression (default)

Each unique value from a column is assigned an id and a dictionary is built that maps the id to the value. The forward index stores bit-compressed ids instead of the values. If you have few unique values, dictionary-encoding can significantly improve space efficiency.

The below diagram shows the dictionary encoding for two columns with `integer` and `string` types. For`colA`, dictionary encoding saved a significant amount of space for duplicated values.

On the other hand, `colB` has no duplicated data. Dictionary encoding will not compress much data in this case where there are a lot of unique values in the column. For the `string` type, we pick the length of the longest value and use it as the length for the dictionary’s fixed-length value array. The padding overhead can be high if there are a large number of unique values for a column.

![](<../../.gitbook/assets/dictionary (1).png>)

## Sorted forward index with run-length encoding

When a column is physically sorted, Pinot uses a sorted forward index with run-length encoding on top of the dictionary-encoding. Instead of saving dictionary ids for each document id, Pinot will store a pair of start and end document ids for each value.

![Sorted forward index](../../.gitbook/assets/sorted-forward.png)

(For simplicity, this diagram does not include the dictionary encoding layer.)

The Sorted forward index has the advantages of both good compression and data locality. The Sorted forward index can also be used as an inverted index.

Sorted forward index are active when the following criteria are true:
* The segment is sorted by this column
* The dictionary is enabled for that column (see [dictionary documentation page](dictionary-index.md)).

If you are ingesting multiple segments you will need to make sure that data is sorted within each segment - you don't need to sort the data across segments.

To ensure a segment is sorted by the column, do the following:
* In real-time tables, use `tableIndexConfig.sortedColumn`.
  If there is exactly one column in that array, Pinot sorts the segment by that column when it is committed.
* In offline tables, `tableIndexConfig.sortedColumn` is ignored and you will need to sort the data by that column before
  ingesting it into Pinot.

When a real-time segment is committed and when an offline segment created, Pinot will do a pass over the data in each 
column and consider sorted any column that contains sorted data, even if they aren't specified as the `sortedColumn`.

Use the following table config as an example:

{% code title="Part of a tableConfig" %}
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
{% endcode %}

{% hint style="info" %}
**Remember that**: 
* Although `sortedColumns` expects an array, only 1 sorted column can be added.
* `tableIndexConfig.sortedColumn` is only honored in real-time tables
* The sorted property affects Pinot behavior beyond forward index.
  For example, sorted segments behaves better on queries that order by in-segment sorted columns.
{% endhint %}

### Checking sort status

You can check the sorted status of a column in a segment by running the following:

```bash
$ grep memberId <segment_name>/v3/metadata.properties | grep isSorted
column.memberId.isSorted = true
```

Alternatively, for offline tables and for committed segments in real-time tables, you can retrieve the sorted status from the _getServerMetadata_ endpoint. The following example is based on the [Batch Quick Start](../getting-started/quick-start.md#batch):

```
curl -X GET \
  "http://localhost:9000/segments/baseballStats/metadata?columns=playerID&columns=teamID" \
  -H "accept: application/json" 2>/dev/null | \
  jq -c  '.[] | . as $parent |  
          .columns[] | 
          [$parent .segmentName, .columnName, .sorted]'
```

```
["baseballStats_OFFLINE_0","teamID",false]
["baseballStats_OFFLINE_0","playerID",false]
```

## Raw value forward index

The raw value forward index directly stores values instead of ids.

Without the dictionary, the dictionary lookup step can be skipped for each value fetch. The index can also take advantage of the good locality of the values, thus improving the performance of scanning a large number of values.

The raw value forward index works well for columns that have a large number of unique values where a dictionary does not provide much compression.

As seen in the above diagram, using dictionary encoding will require a lot of random accesses of memory to do those dictionary look-ups. With a raw value forward index, we can scan values sequentially, which can result in improved query performance when applied appropriately.

![](../../.gitbook/assets/no-dictionary.png)

The raw format will be used either:
* The dictionary is disabled for that column (see [dictionary documentation page](dictionary-index.md)).
* The encoding is set to `RAW` in [field config list](../../configuration-reference/table.md#field-config-list).

Also when this format is used, the following parameters can be configured:

| Parameter              | Default | Description                                                                      |
|------------------------|---------|----------------------------------------------------------------------------------|
| chunkCompressionType   | null    | The compression that will be used.                                               |
| deriveNumDocsPerChunk  | false   | Modifies the behavior when storing variable length values (like string or bytes) |
| rawIndexWriterVersion  | 2       | The version initially used                                                       |

The `chunkCompressionType` parameter has the following valid values:
- `PASS_THROUGH`
- `SNAPPY`
- `ZSTANDARD`
- `LZ4`
- `LZ4_LENGTH_PREFIXED`
- `null` (the JSON null value, not `"null"`), which is the default.
  In this case `PASS_THROUGH` will be used for metrics and `LZ4` for other columns

`deriveNumDocsPerChunk` is only used when the datatype may have a variable length.
For example with `string`, `big decimal`, `bytes`, etc.
By default, Pinot uses a fixed number of elements that was chosen empirically.
If changed to true, Pinot will use a heuristic value that depends on the column data.

`rawIndexWriterVersion` changes the algorithm used under the hood to create the index.
This changes the actual data layout, but modern versions of Pinot can read indexes written in older versions.
The latest version right now is 4.

### Configuration

The recommended way to configure the forward index using raw format is the following:

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "tableName": "somePinotTable",
  "fieldConfigList": [
    {
      "name": "playerID",
      "encodingType": "RAW",
      "indexes": {
        "forward": {
          "chunkCompressionType": "PASS_THROUGH", // or "SNAPPY", "ZSTANDARD", "LZ4" or "LZ4_LENGTH_PREFIXED"
          "deriveNumDocsPerChunk": false,
          "rawIndexWriterVersion": 2
        }
      }
    },
    ...
  ],
...
}
```
{% endcode %}

Remember this format can be enabled even if `encodingType` is not defined by explicitly disabling the dictionary index
(see [dictionary documentation page](dictionary-index.md)).  

#### Deprecated

There is another way to configure the raw format parameters:
* chunkCompressionType: Can be defined as a sibling of `name` and `encodingType` in fieldConfigList section.
* deriveNumDocsPerChunk: Can be configured with the property `deriveNumDocsPerChunkForRawIndex`. 
  Remember that in `properties` all values have to be strings, so valid values are `"true"` and `"false"`. 
* rawIndexWriterVersion: Can be configured with the property `rawIndexWriterVersion`.
  Remember that in `properties` all values have to be strings, so valid values are `"2"`, `"3"`, etc.

This is the older way to configure these parameters and although it is not recommended, it can still be used and there 
is no plans to remove it.
In case new parameters are added, they may only be configured in the `forward` JSON object.

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "tableName": "somePinotTable",
  "fieldConfigList": [
    {
      "name": "playerID",
      "encodingType": "RAW",
      "chunkCompressionType": "PASS_THROUGH", // it can also be defined here
      "properties": {
        "deriveNumDocsPerChunkForRawIndex": "false", // here the string value has to be used
        "rawIndexWriterVersion": "2" // here the string value has to be used
      }
    },
    ...
  ],
...
}
```
{% endcode %}

## Dictionary encoded vs raw value

When working out whether a column should use dictionary encoded or raw value encoding, the following comparison table may help:

| Dictionary                                                                  | Raw Value                                                                             |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Provides compression when low to medium cardinality.                        | Eliminates padding overhead                                                           |
| Allows for indexing (esp inv index).                                        | No inv index (only JSON/Text/FST index)                                               |
| Adds one level of dereferencing, so can increase disk seeks                 | Eliminates additional dereferencing, so good when all docs of interest are contiguous |
| For Strings, adds padding to make all values equal length in the dictionary | Chunk de-compression overhead with docs selected don't have spatial locality          |

## Disabling the forward index

Traditionally the forward index has been a mandatory index for all columns in the on-disk segment file format.&#x20;

However, certain columns may only be used as a filter in the `WHERE` clause for all queries. In such scenarios the forward index is not necessary as essentially other indexes and structures in the segments can provide the required SQL query functionality. Forward index just takes up extra storage space for such scenarios and can ideally be freed up.&#x20;

Thus, to provide users an option to save storage space, a knob to disable the forward index is now available.&#x20;

Forward index on one or more columns(s) in your Pinot table can be disabled with the following limitations:

* Only supported for immutable (offline) segments.
* If the column has a [range index](./range-index.md) then the column must be of single-value type and use range index version 2.
* MV columns with duplicates within a row will lose the duplicated entries on forward index regeneration. The ordering of data with an MV row may also change on regeneration. A backfill is required in such scenarios (to preserve duplicates or ordering).
* If forward index regeneration support on reload (i.e. re-enabling the forward index for a forward index disabled column) is required then the dictionary and inverted index must be enabled on that particular column.

Sorted columns will allow the forward index to be disabled, but this operation will be treated as a no-op and the index (which acts as both a forward index and inverted index) will be created.

Like all indexes, forward index can be disabled in `fieldConfigList` explicitly setting the `disabled` property to true:

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "tableName": "somePinotTable",
  "fieldConfigList": [
    {
      "name":"columnA",
      "indexes": {
        "forward": {
          "disabled": true
        }
      }
    },
    ...
  ],
  ...
}
```
{% endcode %}

The older way to do so is still supported, but not recommended.

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
"fieldConfigList":[
  {
     "name":"columnA",
     "properties": {
        "forwardIndexDisabled": "true"
      }
  }
]
```
{% endcode %}


A table reload operation must be performed for the above config to take effect. Enabling / disabling other indexes on the column can be done via the usual [table config](../../configuration-reference/table.md) options.

The forward index can also be regenerated for a column where it is disabled by removing enable the index again and reloading the segment. The forward index can only be regenerated if the dictionary and inverted index have been enabled for the column. If either have been disabled then the only way to get the forward index back is to regenerate the segments via the offline jobs and re-push / refresh the data.

{% hint style="danger" %}
**Warning:**&#x20;

For multi-value (MV) columns the following invariants cannot be maintained after regenerating the forward index for a forward index disabled column:

* Ordering guarantees of the MV values within a row
* If entries within an MV row are duplicated, the duplicates will be lost. Please regenerate the segments via your offline jobs and re-push / refresh the data to get back the original MV data with duplicates.

We will work on removing the second invariant in the future.
{% endhint %}

Examples of queries which will fail after disabling the forward index for an example column, `columnA`, can be found below:

### Select

Forward index disabled columns cannot be present in the `SELECT` clause even if filters are added on it.

```
SELECT columnA
FROM myTable
    WHERE columnA = 10
```

```
SELECT *
FROM myTable
```

### Group By Order By

Forward index disabled columns cannot be present in the `GROUP BY` and `ORDER BY` clauses. They also cannot be part of the `HAVING` clause.

```
SELECT SUM(columnB)
FROM myTable
GROUP BY columnA
```

```
SELECT SUM(columnB), columnA
FROM myTable
GROUP BY columnA
ORDER BY columnA
```

```
SELECT MIN(columnA)
FROM myTable
GROUP BY columnB
HAVING MIN(columnA) > 100
ORDER BY columnB
```

### Aggregation Queries

A subset of the aggregation functions do work when the forward index is disabled such as `MIN`, `MAX`, `DISTINCTCOUNT`, `DISTINCTCOUNTHLL` and more. Some of the other aggregation functions will not work such as the below:&#x20;

```
SELECT SUM(columnA), AVG(columnA)
FROM myTable
```

```
SELECT MAX(ADD(columnA, columnB))
FROM myTable
```

### Distinct

Forward index disabled columns cannot be present in the `SELECT DISTINCT` clause.

```
SELECT DISTINCT columnA
FROM myTable
```

### Range Queries

To run queries on single-value columns where the filter clause contains operators such as `>`, `<`, `>=`, `<=` a version 2 range index must be present. Without the range index such queries will fail as shown below:

```
SELECT columnB
FROM myTable
    WHERE columnA > 1000
```
