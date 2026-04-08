---
description: This section contains reference documentation for the EXPRMIN function.
---

# EXPRMIN

Projects one or more columns from the row where a measuring column has its minimum value. Similar to ARG\_MIN but supports projecting multiple expression columns at once.

## Signature

> EXPRMIN(measureCol, exprCol1, exprCol2, ...)

Parameters:

| Parameter | Description |
| --------- | ----------- |
| `measureCol` | The column whose minimum value determines which row to project from |
| `exprCol1, exprCol2, ...` | One or more columns to project from the row with the minimum measure |

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select EXPRMIN(hits, playerName, yearID) AS value
from baseballStats
WHERE hits > 0
```

| value                   |
| ----------------------- |
| [Ed Fusselback, 1882]   |
