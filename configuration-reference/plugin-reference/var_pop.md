---
description: This section contains reference documentation for the VAR_POP function.
---

# VAR\_POP

Returns the population variance of a numerical column.

## Signatures

`VAR_POP(col1) -> double`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT VAR_POP(numberOfGames) AS variance 
FROM baseballStats
```
