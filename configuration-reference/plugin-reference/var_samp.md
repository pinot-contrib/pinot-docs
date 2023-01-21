---
description: This section contains reference documentation for the VAR_SAMP function.
---

# VAR\_SAMP

Returns the sample variance of a numerical column.

## Signatures

`VAR_SAMP(col1) -> double`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT VAR_SAMP(numberOfGames) AS variance 
FROM baseballStats
```
