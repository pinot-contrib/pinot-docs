---
description: This section contains reference documentation for the SKEWNESS function.
---

# SKEWNESS

Returns the skewness of values in a group as `Double`. Skewness measures the asymmetry of a distribution. A positive skewness indicates a right-skewed distribution, while a negative skewness indicates a left-skewed distribution.

## Signature

> SKEWNESS(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select SKEWNESS(hits) AS value
from baseballStats
WHERE hits > 0
```

| value             |
| ----------------- |
| 3.427189313498882 |
