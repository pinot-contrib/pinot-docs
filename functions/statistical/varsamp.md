---
description: This section contains reference documentation for the VARSAMP function.
---

# VARSAMP

Returns the sample variance of values in a group as `Double`. Sample variance measures the average of the squared deviations from the mean, using Bessel's correction (dividing by N-1 instead of N).

## Signature

> VARSAMP(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select VARSAMP(hits) AS value
from baseballStats
WHERE hits > 0
```

| value              |
| ------------------ |
| 1234.5812          |
