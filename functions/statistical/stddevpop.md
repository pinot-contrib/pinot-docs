---
description: This section contains reference documentation for the STDDEVPOP function.
---

# STDDEVPOP

Returns the population standard deviation of values in a group as `Double`. This is the square root of the population variance.

## Signature

> STDDEVPOP(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select STDDEVPOP(hits) AS value
from baseballStats
WHERE hits > 0
```

| value             |
| ----------------- |
| 35.13642          |
