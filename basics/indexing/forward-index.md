# Forward index

The forward index is the mechanism Pinot employs to store the values of each column. 
At a conceptual level, the forward index can be thought of as a mapping from document IDs (also known as row indices) 
to the actual column values of each row. 

Forward indexes are enabled by default, meaning that columns will have a forward index unless explicitly disabled.
Disabling the forward index can save storage space when other indexes sufficiently cover the required data patterns.
For information on how to disable the forward index and its implications, refer to
[Disabling the Forward Index](forward-index.md#disabling-the-forward-index).

## Dictionary encoded vs raw value

How forward indexes are implemented depends on the index encoding and whether the column is sorted.

When the encoding is set to `RAW`, the forward index is implemented as an array, where the indices correspond to 
document IDs and the values represent the actual row values. 
For more details, refer to the [raw value forward index](forward-index.md#raw-value-forward-index) section.

In the case of `DICTIONARY` encoding, the forward index doesn't store the actual row values but instead stores 
dictionary IDs. 
This introduces an additional level of indirection when reading values, but it allows for more efficient physical 
layouts when unique number of values in the column is significantly smaller than the number of rows. 

The `DICTIONARY` encoding can be even more efficient if the segment is sorted by the indexed column.
You can learn more about the 
[dictionary encoded forward index](forward-index.md#dictionary-encoded-forward-index-with-bit-compression-default) and 
the [sorted forward index](forward-index.md#sorted-forward-index-with-run-length-encoding) in their respective sections.

When working out whether a column should use dictionary encoded or raw value encoding, the following comparison table may help:

| Dictionary                                                                  | Raw Value                                                                             |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Provides compression when low to medium cardinality.                        | Eliminates padding overhead                                                           |
| Allows for indexing (esp inv index).                                        | No inv index (only JSON/Text/FST index)                                               |
| Adds one level of dereferencing, so can increase disk seeks                 | Eliminates additional dereferencing, so good when all docs of interest are contiguous |
| For Strings, adds padding to make all values equal length in the dictionary | Chunk de-compression overhead with docs selected don't have spatial locality          |

### Dictionary-encoded forward index with bit compression (default)

In this approach, each unique value in a column is assigned an ID, and a dictionary is constructed to map these IDs back
to their corresponding values.
Instead of storing the actual values, the default forward index stores these bit-compressed IDs.
This method is particularly effective when dealing with columns containing few unique values, 
as it significantly improves space efficiency.

The below diagram shows the dictionary encoding for two columns with `integer` and `string` types. For`colA`, dictionary encoding saved a significant amount of space for duplicated values.

The diagram below illustrates dictionary encoding for two columns with different data types (integer and string). 
For `colA`, dictionary encoding leads to significant space savings due to duplicated values. 
However, for `colB`, which contains mostly unique values, the compression effect is limited, and padding overhead may 
be high.

![](<../../.gitbook/assets/dictionary (1).png>)

To know more about dictionary encoding, see [Dictionary index](dictionary-index.md).

### Sorted forward index with run-length encoding

When a column is physically sorted, Pinot employs a sorted forward index with run-length encoding, 
which builds upon dictionary encoding. 
Instead of storing dictionary IDs for each document ID, this approach stores pairs of start and end document IDs for 
each unique value.

![Sorted forward index](../../.gitbook/assets/sorted-forward.png)

(For simplicity, this diagram does not include the dictionary encoding layer.)

Sorted forward indexes offer the benefits of efficient compression and data locality and can also serve as an inverted 
index. 
They are active when two conditions are met: the segment is sorted by the column, and the dictionary is enabled for that
column. 
Refer to the [dictionary documentation](dictionary-index.md) for details on enabling the dictionary.

When dealing with multiple segments, it's crucial to ensure that data is sorted within each segment. Sorting across segments is not necessary.

To guarantee that a segment is sorted by a particular column, follow these steps:
- For real-time tables, use the `tableIndexConfig.sortedColumn` property. 
  If there is exactly one column specified in that array, Pinot will sort the segment by that column upon committing.
- For offline tables, you must pre-sort the data by the specified column before ingesting it into Pinot. 

{% hint style="warning" %}
It's crucial to note that for offline tables, the `tableIndexConfig.sortedColumn` property is indeed ignored. 

Additionally, for online tables, even though this property is specified as a JSON array, at most one column should be 
included. 
Using an array with more than one column is incorrect and will not result in segments being sorted by all the columns 
listed in the array.
{% endhint %}

When a real-time segment is committed, rows will be sorted by the sorting column and it will be transformed into an
offline segment.

During the creation of an offline segment, which also applies when a real-time segment is committed, Pinot scans the 
data in each column. 
If it detects that all values within a column are sorted in ascending order, Pinot concludes that the segment is sorted 
based on that particular column.
In case this happens on more than one column, all of them are considered as sorting columns.
Consequently, whether a segment is sorted by a column or not solely depends on the actual data distribution within the 
segment and entirely disregards the value of the `sortedColumn` property.
This approach also implies that two segments belonging to the same table may have a different number of sorting columns.
In the extreme scenario where a segment contains only one row, Pinot will consider all columns within that segment as 
sorting columns.

Here is an example of a table configuration that illustrates these concepts:

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

#### Checking sort status

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

### Raw value forward index

The raw value forward index stores actual values instead of IDs. 
This means that it eliminates the need for dictionary lookups when fetching values, which can result in improved 
query performance. 
Raw forward index is particularly effective for columns with a large number of unique values, where dictionary encoding
doesn't provide significant compression benefits.

As shown in the diagram below, dictionary encoding can lead to numerous random memory accesses for dictionary lookups. 
In contrast, the raw value forward index allows for sequential value scanning, which can enhance query performance when
applied appropriately.

![](../../.gitbook/assets/no-dictionary.png)

The raw format is used in two scenarios:
1. When the dictionary is disabled for a column, as specified in the [dictionary documentation](dictionary-index.md).
2. When the encoding is set to `RAW` in the [field config list](../../configuration-reference/table.md#field-config-list).

When using the raw format, you can configure the following parameters:

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
  In this case, `PASS_THROUGH` will be used for metrics and `LZ4` for other columns.

`deriveNumDocsPerChunk` is only used when the datatype may have a variable length, 
such as with `string`, `big decimal`, `bytes`, etc. 
By default, Pinot uses a fixed number of elements that was chosen empirically. 
If changed to true, Pinot will use a heuristic value that depends on the column data.

`rawIndexWriterVersion` changes the algorithm used under the hood to create the index.
This changes the actual data layout, but modern versions of Pinot can read indexes written in older versions.
The latest version right now is 4.

#### Raw forward index configuration

The recommended way to configure the forward index using raw format is by including the parameters explained above
in the `indexes.forward` object.
For example:

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
##### Deprecated

An alternative method to configure the raw format parameters is available. 
This older approach can still be used, although it is not recommended. 
Here are the details of this older method:

- `chunkCompressionType`: This parameter can be defined as a sibling of `name` and `encodingType` in the 
  `fieldConfigList` section.
- `deriveNumDocsPerChunk`: You can configure this parameter with the property `deriveNumDocsPerChunkForRawIndex`. 
  Please note that in `properties`, all values must be strings, so valid values for this property are `"true"` and `"false"`.
- `rawIndexWriterVersion`: This parameter can be configured using the property `rawIndexWriterVersion`. 
  Again, in `properties`, all values must be strings, so valid values for this property are `"2"`, `"3"`, and so on.

For example:

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

While this older method is still supported, it is not the recommended way to configure these parameters.
There are no plans to remove support for this older method, but keep in mind that any new parameters added in the future
may only be configurable in the `forward` JSON object.

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

The forward index can also be regenerated for a column where it is disabled by enabling the index and reloading the segment. The forward index can only be regenerated if the dictionary and inverted index have been enabled for the column. If either have been disabled then the only way to get the forward index back is to regenerate the segments via the offline jobs and re-push / refresh the data.

{% hint style="danger" %}
**Warning:**&#x20;

For multi-value (MV) columns the following invariants cannot be maintained after regenerating the forward index for a forward index disabled column:

* Ordering guarantees of the MV values within a row
* If entries within an MV row are duplicated, the duplicates will be lost. Regenerate the segments via your offline jobs and re-push / refresh the data to get back the original MV data with duplicates.

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
