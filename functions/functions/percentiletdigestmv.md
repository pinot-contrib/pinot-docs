---
description: >-
  This section contains reference documentation for the PERCENTILETDIGESTMV
  function.
---

# percentiletdigestmv

Returns the Nth percentile of the group using [T-digest algorithm](https://raw.githubusercontent.com/tdunning/t-digest/master/docs/t-digest-paper/histo.pdf). An optional compression\_factor can be specified to control the accuracy with a tradeoff in memory usage (i.e. higher compression\_factor gives better accuracy but takes more memory). The default compression\_factor is 100.

## Signature

> PERCENTILETDIGESTMV(colName, percentile)
>
> PERCENTILETDIGESTMV(colName, percentile, compression\_factor)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select PERCENTILETDIGESTMV(DivLongestGTimes, 50, 1000) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 10    |

```sql
select PERCENTILETDIGESTMV(DivLongestGTimes, 90) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 44    |

```sql
select PERCENTILETDIGESTMV(DivLongestGTimes, 99.9) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 108   |
