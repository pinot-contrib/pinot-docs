---
description: This section contains reference documentation for the IDSET function.
---

# IDSET

Returns a serialized IdSet representing the set of distinct values for a column. The IdSet can be backed by a RoaringBitmap (for INT columns), Roaring64NavigableMap (for LONG columns), or BloomFilter (for other types). The serialized IdSet is useful with the `IN_ID_SET` filter for efficient precomputed filtering.

Optional parameters can configure the IdSet type and properties.

## Signature

> IDSET(colName)
>
> IDSET(colName, 'parameters')

Supported parameters (semicolon-separated):

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`sizeThresholdInBytes`</td>
      <td>Maximum size before switching to BloomFilter</td>
      <td>8MB</td>
    </tr>
    <tr>
      <td>`expectedInsertions`</td>
      <td>Expected number of insertions for BloomFilter</td>
      <td>5000000</td>
    </tr>
    <tr>
      <td>`fpp`</td>
      <td>False positive probability for BloomFilter</td>
      <td>0.03</td>
    </tr>
  </tbody>
</table>

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select IDSET(playerID) AS value
from baseballStats
WHERE yearID = 2000
```

```sql
select IDSET(playerID, 'sizeThresholdInBytes=1048576;expectedInsertions=5000000;fpp=0.03') AS value
from baseballStats
```

The resulting IdSet can be used in subsequent queries:

```sql
select playerName
from baseballStats
WHERE IN_ID_SET(playerID, '<base64-encoded-idset>') = 1
```
