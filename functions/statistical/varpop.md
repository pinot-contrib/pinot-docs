---
description: This section contains reference documentation for the VARPOP function.
---

# VARPOP

Returns the population variance of values in a group as `Double`. Population variance measures the average of the squared deviations from the mean across the entire population.

## Signature

> VARPOP(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select VARPOP(hits) AS value
from baseballStats
WHERE hits > 0
```

| value              |
| ------------------ |
| 1234.5678          |
