---
description: This section contains reference documentation for the percentileest function.
---

# percentileest

Returns the Nth percentile of the group using [Quantile Digest](https://github.com/airlift/airlift/blob/master/stats/src/main/java/io/airlift/stats/QuantileDigest.java) algorithm.

## Signature

> percentileest(colName, percentile)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select percentileest(homeRuns, 50) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 0 | 

```sql
select percentileest(homeRuns, 80) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 4 | 

```sql
select percentileest(homeRuns, 99.9) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 46 | 