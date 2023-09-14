# Dictionary index

When dealing with extensive datasets, it's common for values to be repeated multiple times.
To enhance storage efficiency and reduce query latencies, we strongly recommend employing a 
dictionary index for repetitive data.
This is the reason Pinot enables dictionary encoding by default, 
even though it is advisable to disable it for columns with high cardinality. 

## Influence on other indexes

In Pinot, dictionaries serve as both an index and actual encoding. 
Consequently, when dictionaries are enabled, the behavior or layout of certain other indexes undergoes modification. 
The relationship between dictionaries and other indexes is outlined in the following table:

| Index                                       | Conditional               | Description                                                         |
|---------------------------------------------|---------------------------|---------------------------------------------------------------------|
| [forward](forward-index.md)                 |                           | Implementation depends on whether the dictionary is enabled or not. |
| [range](range-index.md)                     |                           | Implementation depends on whether the dictionary is enabled or not. |
| [inverted](inverted-index.md)               |                           | Requires dictionary.                                                |
| [json](json-index.md)                       | when `optimizeDictionary` | Disables dictionary.                                                |
| [text](text-search-support.md)              | when `optimizeDictionary` | Disables dictionary.                                                |
| FST                                         |                           | Requires dictionary.                                                |
| [H3 (or geospatial)](geospatial-support.md) |                           | Incompatible with dictionary.                                       |


## Configuration

### Enable or disable dictionaries
Unlike many other indexes, dictionary indexes are enabled by default, under the assumption that the count of unique 
values will be significantly lower than the number of rows.

If this assumption does not hold true, you can deactivate the dictionary for a specific column by setting the `disabled`
property to true within `indexes.dictionary`:

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "theTableName",
      "indexes": {
        "dictionary": {
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

You may choose the option you prefer, but it's essential to maintain consistency, as Pinot will reject table 
configurations where the same column and index are defined in different locations.

The decision of whether to create the dictionary or not can be left to certain built-in Pinot heuristics.
This functionality can be enabled within the `indexingConfig` object within the table configuration. 
The parameters that govern these heuristics are:

| Parameter                      | Default | Description                                                           |
|--------------------------------|---------|-----------------------------------------------------------------------|
| optimizeDictionary             | false   | Enables the heuristic for all columns and activates some extra rules. |
| optimizeDictionaryForMetrics   | false   | Enables the heuristic for metric columns.                             |
| noDictionarySizeRatioThreshold | 0.85    | The ratio used in the heuristics.                                     |

It's important to emphasize that these parameters are configured for all columns within the table.

When this optimization is enabled, columns explicitly marked as dictionaries will be encoded as raw
if all the following criteria are true:

- They are not multi-valued.
- Their column type is fixed size (such as int, long, double, timestamp, etc).
- The ratio between the forward index size encoded as raw and the forward index size encoded as a dictionary is less
  than `noDictionarySizeRatioThreshold`

If `optimizeDictionary` is set to false and `optimizeDictionaryForMetrics` is true, only columns declared as metrics 
will be affected.

If `optimizeDictionary` is set to true, all columns will be affected.
In this scenario, columns indexed as [text](./text-search-support.md) or [JSON](./json-index.md) will automatically be 
indexed as raw.

Please note that `optimizeDictionary` takes precedence over `optimizeDictionaryForMetrics`, and the special rule 
applied to text and JSON indexes only applies when `optimizeDictionary` is true.

### Parameters

Dictionaries can be configured with the following options 

| Parameter              | Default | Description                                                       |
|------------------------|---------|-------------------------------------------------------------------|
| onHeap                 | false   | Specifies whether the index should be loaded on heap or off heap. |
| useVarLengthDictionary | false   | Determines how to store variable-length values.                   |

Dictionaries are always off heap, but in cases where the cardinality is small and the footprint on heap is acceptably 
small, they can be copied in memory by changing `onHeap` parameter to true.
When they are on heap, dictionaries can be faster and some extra optimizations can be done.

Dictionaries are always stored off-heap. 
However, in cases where the cardinality is small, and the on-heap memory usage is acceptable, 
you can copy them into memory by setting the `onHeap` parameter to true. 
When dictionaries are on-heap, they can offer improved performance, and additional optimizations become possible.

The `useVarLengthDictionary` parameter only impacts columns with values that vary in the number of bytes they occupy.
This includes column types that require a variable number of bytes, such as strings, bytes, or big decimals, 
and scenarios where not all values within a segment occupy the same number of bytes. 
For example, even strings in general require a variable number of bytes to be stored, 
if a segment contains only the values "a", "b", and "c" Pinot will identify that all values in the segment 
can be represented with the same number of bytes.

By default, `useVarLengthDictionary` is set to `false`, which means Pinot will calculate the length of the largest value
contained within the segment. 
This length will then be used for all values. 
This approach ensures that all values can be stored efficiently, resulting in faster access and a more compressed layout 
when the lengths of values are similar.

If your dataset includes a few very large values and a multitude of very small ones, 
it is advisable to instruct Pinot to utilize variable-length encoding by setting `useVarLengthDictionary` to `true`.
When variable encoding is employed, Pinot is required to store the length of each entry.
Consequently, the cost of storing an entry becomes its actual size plus an additional 4 bytes for the offset.