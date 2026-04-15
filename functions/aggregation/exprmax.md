---
description: This section contains reference documentation for the EXPRMAX function.
---

# EXPRMAX

Projects one or more columns from the row where a measuring column has its maximum value. Similar to ARG\_MAX but supports projecting multiple expression columns at once.

## Signature

> EXPRMAX(measureCol, exprCol1, exprCol2, ...)

Parameters:

| Parameter | Description |
| --------- | ----------- |
| `measureCol` | The column whose maximum value determines which row to project from |
| `exprCol1, exprCol2, ...` | One or more columns to project from the row with the maximum measure |

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select EXPRMAX(hits, playerName, yearID) AS value
from baseballStats
```

| value                  |
| ---------------------- |
| [Ichiro Suzuki, 2004]  |
