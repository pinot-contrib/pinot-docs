---
description: This section contains reference documentation for the sum function.
---

# sum

Get the sum of values in a group

## Signature

> SUM(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select sum(hits) AS value
from baseballStats 
```

| value   |
| ------- |
| 3692601 |
