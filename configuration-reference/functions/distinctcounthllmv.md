---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLLMV
  function.
---

# DISTINCTCOUNTBITMAPMV

Returns an approximate distinct count using HyperLogLog in a group.

## Signature

> DISTINCTCOUNTHLLMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DISTINCTCOUNTHLLMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 34    |
