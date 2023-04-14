# Dictionary Index

When storing large amounts of data, most of the time the values are repeated several times.
In order to optimize the storage and query latencies in this case, Pinot can be configured to use a dictionary.

## Influence on other indexes

Dictionaries are not only an index but an actual encoding in Pinot.
That means that when they are enabled, some other indexes change their behavior or layout.
The relation between dictionary and other indexes is the following:

| Index                                       | Conditional               | Description                                                         |
|---------------------------------------------|---------------------------|---------------------------------------------------------------------|
| [forward](forward-index.md)                 |                           | Implementation depends on whether the dictionary is enabled or not. |
| [range](range-index.md)                     |                           | Implementation depends on whether the dictionary is enabled or not. |
| [inverted](inverted-index.md)               |                           | Requires dictionary.                                                |
| [json](json-index.md)                       | when `optimizeDictionary` | Disables dictionary.                                                |
| [text](text-search-support.md)              | when `optimizeDictionary` | Disables dictionary.                                                |
| FST                                         |                           | Requires dictionary.                                                |
| [H3 (or geospatial)](geospatial-support.md) |                           | Requires no dictionary.                                             |


## Configuration

### How to enable or disable dictionaries
Unlike most indexes, dictionary indexes are enabled by default, assuming that the number of unique values will
be orders of magnitude smaller than the number of rows.

If this is not the case, it is recommended to disable the dictionary for the column.
In order to that, use the `disabled` property in `indexes.dictionary`:

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "theTableName",
      "indexes": {
        "dictioanry": {
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

Alternatively, the `encodingType` property can be changed. For example:
```javascript
{
  "fieldConfigList": [
    {
      "name": "theTableName",
      "encodingType": "RAW"
    },
    ...
  ],
...
}
```
{% endcode %}

Use the option you prefer, but try to be consistent, as Pinot will reject table configurations where the same column and
index is defined in different places.

The decision of actually create the dictionary or not can be delegated to some included Pinot heuristics.
This feature can be enabled in `indexingConfig` object inside table config.
The parameters that control the heuristic are:


| Parameter                      | Default | Description                                                          |
|--------------------------------|---------|----------------------------------------------------------------------|
| optimizeDictionary             | false   | Enables the heuristic for all columns and activate some extra rules. |
| optimizeDictionaryForMetrics   | false   | Enables the heuristic for metric columns.                            |
| noDictionarySizeRatioThreshold | 0.85    | The ratio used in the heuristics.                                    |

It is important to note that these parameters are configured for all columns on the table.
When this optimization is enabled, columns explicitly marked as dictionary will actually be encoded as raw 
if:
- They are not multi-valued.
- And their column type is fixed size (like int, long, double, timestamp, etc).
- And their ratio between the forward index size encoded as raw and the forward index size encoded as dictionary is lower than `noDictionarySizeRatioThreshold`.

If `optimizeDictionary` is false and `optimizeDictionaryForMetrics` is true, only columns declared as metric will be affected.
If `optimizeDictionary` is true, all columns will be affected.
Also in this case columns indexed as [text](./text-search-support.md) or [JSON](./json-index.md) will automatically be indexed as raw.
Note that `optimizeDictionary` has priority over `optimizeDictionaryForMetrics` and the special rule applied to text 
and JSON indexes only applies when `optimizeDictionary` is true.

### Parameters

There are some options you can configure:

| Parameter              | Default | Description                                    |
|------------------------|---------|------------------------------------------------|
| onHeap                 | false   | If the index must be load on heap or off heap. |
| useVarLengthDictionary | false   | How to store variable length values.           |

Dictionaries are always off heap, but in cases where the cardinality is small and the footprint on heap is acceptably 
small, they can be copied in memory by changing `onHeap` parameter to true.
When they are on heap, dictionaries can be faster and some extra optimizations can be done.

Parameter `useVarLengthDictionary` only affects columns whose values require variable number of bytes.
That means that:
* The column type requires variable number of bytes (like string, bytes or big decimal).
* Not all values on the segment require the same number of bytes.
  For example, if the segment only contains values "a", "b" and "c", Pinot will detect that there all values
  can be represented with the same number of bytes.

By default, this parameter is `false`, which means that Pinot will calculate the larger value contained in the segment.
That is the length that will be used for each value.
This guarantees that all values can be stored and produce faster access and a more compressed layout when the length of
values are quite similar.

This default is not great when there are a few very large values and a lot of very small ones.
In that case it is recommended to indicate Pinot to use a variable length encoding by setting `useVarLengthDictionary` to `true`.
When the variable encoding is used, Pinot needs to store the entry length, so the cost of storing an entry is
their actual size plus 4 bytes offset.

### When dictionaries are created
Although dictionaries are enabled by default, they are usually not created at 