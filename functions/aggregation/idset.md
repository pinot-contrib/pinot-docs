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

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `sizeThresholdInBytes` | Maximum size before switching to BloomFilter | 8MB |
| `expectedInsertions` | Expected number of insertions for BloomFilter | 5000000 |
| `fpp` | False positive probability for BloomFilter | 0.03 |

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
