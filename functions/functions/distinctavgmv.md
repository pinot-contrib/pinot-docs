---
description: This section contains reference documentation for the DISTINCTAVGMV function.
---

# DISTINCTAVGMV

Returns the average of distinct row values in a group

## Signature

> DISTINCTAVGMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
SELECT DISTINCTAVGMV(DivLongestGTimes) AS VALUE
FROM airlineStats
WHERE arraylength(DivLongestGTimes) > 1
```

| VALUE |
| ----- |
| 32.4  |
