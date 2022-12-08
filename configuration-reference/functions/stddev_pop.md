---
description: This section contains reference documentation for the STDDEV_POP function.
---

# STDDEV\_POP

Returns the population standard deviation of a numerical column.

## Signatures

`STDDEV_POP(col1) -> double`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT STDDEV_POP(numberOfGames) AS stddev 
FROM baseballStats
```
