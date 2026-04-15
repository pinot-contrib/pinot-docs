---
description: This section contains reference documentation for the count function.
---

# count

Get the count of rows in a group

## Signature

> COUNT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select count(*) AS value
from baseballStats 
```

| value |
| ----- |
| 97889 |
