---
description: >-
  This section contains reference documentation for the PERCENTILEESTMV
  function.
---

# percentileestmv

Returns the Nth percentile of the group using [Quantile Digest](https://github.com/airlift/airlift/blob/master/stats/src/main/java/io/airlift/stats/QuantileDigest.java) algorithm.

## Signature

> PERCENTILEESTMV(colName, N)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select PERCENTILEESTMV(DivLongestGTimes, 50) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 10    |

```sql
select PERCENTILEESTMV(DivLongestGTimes, 90) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 44    |

```sql
select PERCENTILEESTMV(DivLongestGTimes, 99.9) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 108   |
