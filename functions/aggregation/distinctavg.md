---
description: This section contains reference documentation for the DISTINCTAVG function.
---

# DISTINCTAVG

Returns the average of distinct row values in a group

## Signature

`DISTINCTAVG(colName) or avg(distinct col)`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT DISTINCTAVG(runs) AS VALUE
FROM baseballStats
```

| VALUE             |
| ----------------- |
| 83.36526946107784 |



```sql
SELECT AVG(DISTINCT AtBatting) AS VALUE
FROM baseballStats
```

| VALUE             |
| ----------------- |
| 349.1158798283262 |

