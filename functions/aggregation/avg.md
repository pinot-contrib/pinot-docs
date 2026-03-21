---
description: This section contains reference documentation for the AVG function.
---

# AVG

Returns the average of values for a numeric column in a group as `Double`.

## Signature

> AVG(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select AVG(hits) AS value
from baseballStats
```

| value              |
| ------------------ |
| 27.254965229242498 |
