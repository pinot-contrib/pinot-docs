---
description: This page describes configuring the Bloom filter for Apache Pinot
---

# Bloom filter

When a column is configured to use this filter, Pinot creates one Bloom filter per segment.
The Bloom filter help to prune segments that do not contain any record matching an **EQUALITY** predicate.

This is useful for a query like the following:

```sql
SELECT COUNT(*) 
FROM baseballStats 
WHERE playerID = 12345
```

## Details

A Bloom filter is a probabilistic data structure used to definitively determine if an element **is not** present in a 
dataset, but it cannot be employed to determine if an element **is** present in the dataset. 
This limitation arises because Bloom filters may produce false positives but never yield false negatives.

An intriguing aspect of these filters is the existence of a mathematical formula that establishes a relationship between
their size, the cardinality of the dataset they index, and the rate of false positives.

In Pinot, this cardinality corresponds to the number of unique values expected within each segment.
If necessary, the false positive rate and the index size can be configured.

## Configuration

Bloom filters are deactivated by default, implying that columns will not be indexed unless they are explicitly 
configured within the [table configuration](../../configuration-reference/table.md).

There are 3 optional parameters to configure the Bloom filter:

| Parameter      | Default       | Description                                                           |
|----------------|---------------|-----------------------------------------------------------------------|
| fpp            | 0.05          | False positive probability of the Bloom filter (from `0` to `1`).     |
| maxSizeInBytes | 0 (unlimited) | Maximum size of the Bloom filter.                                     |
| loadOnHeap     | false         | Whether to load the Bloom filter using heap memory or off-heap memory. |

The lower the `fpp` (false positive probability), the greater the accuracy of the Bloom filter, but this reduction in 
`fpp` will also lead to an increase in the index size.
It's important to note that `maxSizeInBytes` takes precedence over `fpp`.
If `maxSizeInBytes` is set to a value greater than 0 and the calculated size of the Bloom filter, 
based on the specified `fpp`, exceeds this size limit, Pinot will adjust the `fpp` to ensure that the Bloom filter 
size remains within the specified limit.

Similar to other indexes, a Bloom filter can be explicitly deactivated by setting the special parameter `disabled` to 
true.

### Example

For example the following table config enables the Bloom filter in the _playerId_ column using the default values:

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "tableName": "somePinotTable",
  "fieldConfigList": [
    {
      "name": "playerID",
      "indexes": {
        "bloom": {}
      }
    },
    ...
  ],
  ...
}
```
{% endcode %}

In case some parameter needs to be customized, they can be included in `fieldConfigList.indexes.bloom`.
Remember that even the example customizes all parameters, you can just modify the ones you need.

{% code title="Configured in tableConfig fieldConfigList" %}
```javascript
{
  "tableName": "somePinotTable",
  "fieldConfigList": [
    {
      "name": "playerID",
      "indexes": {
        "bloom": {
          "fpp": 0.01,
          "maxSizeInBytes": 1000000,
          "loadOnHeap": true
        }
      }
    },
    ...
  ],
  ...
}
```
{% endcode %}

<details>

<summary>Older configuration</summary>

#### Use default settings

To use default values, include the name of the column in `tableIndexConfig.bloomFilterColumns`.

For example:

{% code title="Part of a tableConfig" %}
```javascript
{
  "tableName": "somePinotTable",
  "tableIndexConfig": {
    "bloomFilterColumns": [
      "playerID",
      ...
    ],
    ...
  },
  ...
}
```
{% endcode %}

#### Customized parameters

To specify custom parameters, add a new entry in `tableIndexConfig.bloomFilterConfig` object.
The key should be the name of the column and the value should be an object similar to the one that can be used in the
Bloom section of `fieldConfigList`.

For example:

{% code title="Part of a tableConfig" %}
```javascript
{
  "tableIndexConfig": {
    "bloomFilterConfigs": {
      "playerID": {
        "fpp": 0.01,
        "maxSizeInBytes": 1000000,
        "loadOnHeap": true
      },
      ...
    },
    ...
  },
  ...
}
```
{% endcode %}

</details>