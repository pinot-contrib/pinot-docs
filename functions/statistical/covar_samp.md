---
description: This section contains reference documentation for the COVAR_SAMP function.
---

# COVAR\_SAMP

Returns the sample covariance between of 2 numerical columns.

```
COVAR_SAMP(col1, col2) = COVAR_POP(col1, col2) * besselCorrection
```

## Signatures

`COVAR_SAMP(col1, col2) -> double`

When advanced null handling is enabled, a row contributes only when both columns are non-null. The function returns `NULL` when no rows contribute or when fewer than two rows contribute, because sample covariance is undefined in those cases. Without advanced null handling, Pinot uses each column's configured default null value.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
SELECT COVAR_SAMP(numberOfGames, AtBatting) AS covariance 
FROM baseballStats
```

| covariance        |
| ----------------- |
| 8270.973200974102 |
