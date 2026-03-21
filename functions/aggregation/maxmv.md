---
description: This section contains reference documentation for the MAXMV function.
---

# MAXMV

Get the maximum value in a group

## Signature

> MAXMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select MAXMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value |
| ----- |
| 108   |
