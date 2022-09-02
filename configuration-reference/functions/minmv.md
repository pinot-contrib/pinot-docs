---
description: This section contains reference documentation for the MINMV function.
---

# MINMV

Get the minimum value in a group

## Signature

> MINMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select MINMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 2     |
