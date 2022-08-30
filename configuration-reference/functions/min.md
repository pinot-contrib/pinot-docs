---
description: This section contains reference documentation for the min function.
---

# min

Get the minimum value in a group

## Signature

> MIN(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select min(yearID) AS value
from baseballStats 
```

| value |
| ----- |
| 1871  |
