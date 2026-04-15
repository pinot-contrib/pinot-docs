---
description: This section contains reference documentation for the STDDEVSAMP function.
---

# STDDEVSAMP

Returns the sample standard deviation of values in a group as `Double`. This is the square root of the sample variance (using Bessel's correction).

## Signature

> STDDEVSAMP(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select STDDEVSAMP(hits) AS value
from baseballStats
WHERE hits > 0
```

| value             |
| ----------------- |
| 35.13680          |
