---
description: >-
This section contains reference documentation for the DISTINCTCOUNTBITMAPMV
function.
---

# DISTINCTCOUNTBITMAPMV

Returns the count of distinct row values in a group. This function is accurate for INT or dictionary encoded column, but approximate for other cases where hash codes are used in distinct counting and there may be hash collision.

## Signature

> DISTINCTCOUNTBITMAPMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DISTINCTCOUNTBITMAPMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 34    |

```sql
select DISTINCTCOUNTBITMAPMV(DivTailNums) AS value
from airlineStats 
where arraylength(DivTailNums) > 1
```

| value |
| ----- |
| 2     |
