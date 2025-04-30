---
description: This section contains reference documentation for the COVAR_POP function.
---

# COVAR\_POP

Returns the population covariance between of 2 numerical columns.

<pre><code><strong>COVAR_POP(col1, col2) = E[col1 * col2] - E[col1]E[col2]</strong></code></pre>

## Signatures

`COVAR_POP(col1, col2) -> double`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT COVAR_POP(numberOfGames, hits) AS covariance 
FROM baseballStats
```

| covariance        |
| ----------------- |
| 2314.249154477403 |
