---
description: This section contains reference documentation for the PERCENTILETDIGESTMV function.
---

# PERCENTILETDIGESTMV

Returns the Nth percentile of the group using [T-digest algorithm](https://raw.githubusercontent.com/tdunning/t-digest/master/docs/t-digest-paper/histo.pdf).


## Signature

> PERCENTILETDIGESTMV(colName, N)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select PERCENTILETDIGESTMV(DivLongestGTimes, 50) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value   | 
| ------------- |
| 10 | 


```sql
select PERCENTILETDIGESTMV(DivLongestGTimes, 90) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value   | 
| ------------- |
| 44 | 


```sql
select PERCENTILETDIGESTMV(DivLongestGTimes, 99.9) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value   | 
| ------------- |
| 108 | 
