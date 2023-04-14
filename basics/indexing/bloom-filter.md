# Bloom Filter

When a column is configured to use this filter, Pinot creates one bloom filter per segment.
Bloom filter helps prune segments that do not contain any record matching an **EQUALITY** predicate.

It would be useful for a query like the following:

```
SELECT COUNT(*) 
FROM baseballStats 
WHERE playerID = 12345
```

## Details

A bloom filter is a probabilistic data structure that can be used to know for a fact if an element **is not** in a 
dataset but they cannot be used to know if an element **is** in a dataset.
The reason for that is that bloom filters return false positives but never return false negatives.

One interesting property of these filters is that there is a mathematical formula that relates their size, 
the cardinality of the dataset they index and the rate of false positives.

In Pinot this cardinality is the number of unique values expected on each segment.
The false positive rate and the size of the index can be configured if needed.

## Configuration

Bloom filters are disabled by default.
This means that columns will not be indexed unless they are explicitly configured in the [table config](../../configuration-reference/table.md).

There are 3 optional parameters to configure the Bloom Filter:

| Parameter      | Default       | Description                                                           |
|----------------|---------------|-----------------------------------------------------------------------|
| fpp            | 0.05          | False positive probability of the bloom filter (from `0` to `1`).     |
| maxSizeInBytes | 0 (unlimited) | Maximum size of the bloom filter.                                     |
| loadOnHeap     | false         | Whether to load the bloom filter using heap memory or off-heap memory |

The lower the `fpp`, the higher accuracy the bloom filter has, but it will also increase the index size.
`maxSizeInBytes` has more priority than `fpp`.
This means that if `maxSizeInBytes` is higher than 0 and `fpp` generates a bloom filter larger than this size, we will 
increase the `fpp` to keep the bloom filter size within this limit.

Like all indexes, a bloom filter can be explicitly disabled by setting the special parameter `disabled` to true. 

### Field config list

As all single column indexes, they should be configured in the field config list using the `bloom` key.

For example the following table config enables the bloom filter in the _playerId_ column:

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


### Deprecated configuration 

Although the recommended way to configure bloom filters is by using `fieldConfigList`, there are other 2 ways to 
configure a bloom filter for a table in the [table config](../../configuration-reference/table.md):

#### Use default settings

In case the default values are the ones that want to be used, include the name of the column in `tableIndexConfig.bloomFilterColumns`.

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

When custom parameters are required, add a new entry in `tableIndexConfig.bloomFilterConfig` object.
The key should be the name of the column and the value should be an object similar to the one that can be used in the
bloom section of `fieldConfigList`.

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