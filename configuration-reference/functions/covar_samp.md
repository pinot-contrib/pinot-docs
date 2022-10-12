---
description: This section contains reference documentation for the COVAR_SAMP function.
---

# COVAR\_SAMP

Returns the sample covariance between of 2 numerical columns.

<pre><code><strong>COVAR_SAMP(col1, col2) = COVAR_POP(col1, col2) * besselCorrection</strong></code></pre>

## Signatures

`COVAR_SAMP(col1, col2) -> double`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT COVAR_SAMP(numberOfGames, AtBatting) AS covariance 
FROM baseballStats
```

| covariance        |
| ----------------- |
| 8270.973200974102 |
