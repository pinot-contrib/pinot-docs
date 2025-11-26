# Dictionary index

When dealing with extensive datasets, it's common for values to be repeated multiple times. To enhance storage efficiency and reduce query latencies, we strongly recommend employing a dictionary index for repetitive data. This is the reason Pinot enables dictionary encoding by default, even though it is advisable to disable it for columns with high cardinality.

## Influence on other indexes

In Pinot, dictionaries serve as both an index and actual encoding. Consequently, when dictionaries are enabled, the behavior or layout of certain other indexes undergoes modification. The relationship between dictionaries and other indexes is outlined in the following table:

| Index                                       | Conditional               | Description                                                         |
| ------------------------------------------- | ------------------------- | ------------------------------------------------------------------- |
| [forward](forward-index.md)                 |                           | Implementation depends on whether the dictionary is enabled or not. |
| [range](range-index.md)                     |                           | Implementation depends on whether the dictionary is enabled or not. |
| [inverted](inverted-index.md)               |                           | Requires the dictionary index to be enabled.                        |
| [json](json-index.md)                       | when `optimizeDictionary` | Disables dictionary.                                                |
| [text](text-search-support.md)              | when `optimizeDictionary` | Disables dictionary.                                                |
| FST                                         |                           | Requires dictionary.                                                |
| [H3 (or geospatial)](geospatial-support.md) |                           | Incompatible with dictionary.                                       |

## Configuration

### Deterministically enable or disable dictionaries

Unlike many other indexes, dictionary indexes are enabled by default, under the assumption that the count of unique values will be significantly lower than the number of rows.

If this assumption does not hold true, you can deactivate the dictionary for a specific column by setting the `disabled` property to true within `indexes.dictionary`:

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "col1",
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
      "name": "col1",
      "encodingType": "RAW"
    },
    ...
  ],
...
}
```

You may choose the option you prefer, but it's essential to maintain consistency, as Pinot will reject table configurations where the same column and index are defined in different locations.

### Heuristically enable dictionaries

Most of the time the domain expert that creates the table knows whether a dictionary will be useful or not. For example, a column with random values or public IPs will probably have a large cardinality, so they can be immediately be targeted as raw encoded while columns like employee ids will have a small cardinality and therefore can be easily be recognized as good dictionary candidates. But sometimes the decision may not be clear. To help in these situations, Pinot can be configured to heuristically create the dictionary depending on the actual values and a relation factor.

When this heuristic is enabled, Pinot calculates a saving factor for each _candidate_ column. This factor is the ratio between the forward index size encoded as raw and the same index encoded as a dictionary. If the saving factor for a _candidate_ column is less than a saving ratio, the dictionary is not created.

In order to be considered as a _candidate_ for the heuristic, a column must:

* Be marked as dictionary encoded (columns marked as raw are always encoded as raw).
* Be single valued (multi-valued columns are never considered by the heuristic).
* Be of a fixed size type such as int, long, double, timestamp, etc. Variable size types like json, strings or bytes are never considered by the heuristic.
* Not indexed by [text index](text-search-support.md) or [JSON index](json-index.md) (as they are only useful when cardinality is very large).

Optionally this feature can be applied only to metric columns, skipping dimension columns.

This functionality can be enabled within the `indexingConfig` object within the table configuration. The parameters that govern these heuristics are:

| Parameter                      | Default | Description                                                           |
| ------------------------------ | ------- | --------------------------------------------------------------------- |
| optimizeDictionary             | false   | Enables the heuristic for all columns and activates some extra rules. |
| optimizeDictionaryForMetrics   | false   | Enables the heuristic for metric columns.                             |
| noDictionarySizeRatioThreshold | 0.85    | The saving ratio used in the heuristics.                              |

It's important to emphasize that:

* These parameters are configured for all columns within the table.
* `optimizeDictionary` takes precedence over `optimizeDictionaryForMetrics`.

### Parameters

Dictionaries can be configured with the following options

| Parameter              | Default      | Description                                                                        |
| ---------------------- | ------------ | ---------------------------------------------------------------------------------- |
| onHeap                 | false        | Specifies whether the index should be loaded on heap or off heap.                  |
| useVarLengthDictionary | false        | Determines how to store variable-length values.                                    |
| intern                 | empty object | Configuration for interning. Only for on-heap dictionaries. Read about that below. |
| intern.capacity        | null         | how many values should be interning                                                |

#### Variable length dictionaries

The `useVarLengthDictionary` parameter only impacts columns with values that vary in the number of bytes they occupy. This includes column types that require a variable number of bytes, such as strings, bytes, or big decimals, and scenarios where not all values within a segment occupy the same number of bytes. For example, even strings in general require a variable number of bytes to be stored, if a segment contains only the values "a", "b", and "c" Pinot will identify that all values in the segment can be represented with the same number of bytes.

By default, `useVarLengthDictionary` is set to `false`, which means Pinot will calculate the length of the largest value contained within the segment. This length will then be used for all values. This approach ensures that all values can be stored efficiently, resulting in faster access and a more compressed layout when the lengths of values are similar.

If your dataset includes a few very large values and a multitude of very small ones, it is advisable to instruct Pinot to utilize variable-length encoding by setting `useVarLengthDictionary` to `true`. When variable encoding is employed, Pinot is required to store the length of each entry. Consequently, the cost of storing an entry becomes its actual size plus an additional 4 bytes for the offset.

#### On-heap dictionaries

Dictionary data is always stored off-heap. In general, it is recommended to keep dictionaries that way. However, in cases where the cardinality is small, and the on-heap memory usage is acceptable, you can copy them into memory by setting the `onHeap` parameter to true.&#x20;

{% hint style="danger" %}
Remember: On-heap dictionaries are not recommended.

On-heap dictionaries can slightly reduce latency but will significantly increase the heap memory used by Pinot and increase garbage collection times, which may result in out of memory issues.
{% endhint %}

When off-heap dictionaries are used, data is deserialized each time it is accessed. This isn't a problem with primitive types (such as int or long), but with complex types (like strings or bytes), this means that the data is deserialized each time it is accessed. On-heap dictionaries solve this problem by keeping the data in memory in deserialized format so no allocations are needed at query time.

However, on-heap dictionaries have a cost in terms of memory usage and that cost is proportional to the number of segments that are accessed concurrently. It is important to note that, as with all other indexes, the dictionary scope is limited to segments. This means that if we have a table with 1,000 segments and a dictionary for a column, we may have 1,000 dictionaries in memory. This can be a waste of memory in cases where unique values are repeated across segments. To solve this problem, Pinot can retain a cache of the dictionary values and reuse them across segments. This cache is not shared between different tables or columns and its maximum size is controlled by the `dictionary.intern.capacity` option.

{% hint style="info" %}
Only string and byte columns can be interned. Pinot ignores the intern configuration when used on columns with a different data type.
{% endhint %}

Here's an example of configuring a dictionary to use on-heap dictionaries with intern mode enabled:

```json
{
  "tableName": "somePinotTable",
  "fieldConfigList": [
    {
      "name": "strColumn",
      "encodingType": "DICTIONARY",
      "indexes": {
        "dictionary": {
          "onHeap": true,
          "intern": {
            "capacity":32000
          }
        }
      }
    }
  ]
}
```
