---
description: This section contains reference documentation for the MINMAXRANGEMV function.
---

# MINMAXRANGEMV

Returns the max - min value in a group

## Signature

> MINMAXRANGEMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select MINMAXRANGEMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 106   |
