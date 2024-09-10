---
description: This section contains reference documentation for the STDDEV_SAMP function.
---

# STDDEV\_SAMP

Returns the sample standard deviation of a numerical column.

## Signatures

`STDDEV_SAMP(col1) -> double`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT STDDEV_SAMP(numberOfGames) AS stddev 
FROM baseballStats
```
