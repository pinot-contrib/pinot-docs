---
description: >-
  This section contains reference documentation for the PERCENTILETDIGEST
  function.
---

# percentiletdigest

Returns the Nth percentile of the group using [T-digest algorithm](https://raw.githubusercontent.com/tdunning/t-digest/master/docs/t-digest-paper/histo.pdf). An optional compression\_factor can be specified to control the accuracy with a tradeoff in memory usage (i.e. higher compression\_factor gives better accuracy but takes more memory). The default compression\_factor is 100.

## Signature

> PERCENTILETDIGEST(colName, percentile)
>
> PERCENTILETDIGEST(colName, percentile, compression\_factor)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select PERCENTILETDIGEST(homeRuns, 50, 1000) AS value
from baseballStats 
```

| value |
| ----- |
| 0     |

```sql
select PERCENTILETDIGEST(homeRuns, 80) AS value
from baseballStats 
```

| value              |
| ------------------ |
| 3.6571905392487856 |

```sql
select PERCENTILETDIGEST(homeRuns, 99.9) AS value
from baseballStats 
```

| value             |
| ----------------- |
| 46.26787306220119 |
