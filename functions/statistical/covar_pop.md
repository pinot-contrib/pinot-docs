---
description: This section contains reference documentation for the COVAR_POP function.
---

# COVAR\_POP

Returns the population covariance between of 2 numerical columns.

```
COVAR_POP(col1, col2) = E[col1 * col2] - E[col1]E[col2]
```

## Signatures

`COVAR_POP(col1, col2) -> double`

When advanced null handling is enabled, a row contributes only when both columns are non-null. The function returns `NULL` when no rows contribute. Without advanced null handling, Pinot uses each column's configured default null value.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
SELECT COVAR_POP(numberOfGames, hits) AS covariance 
FROM baseballStats
```

| covariance        |
| ----------------- |
| 2314.249154477403 |
