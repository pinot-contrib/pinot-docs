---
description: This section contains reference documentation for the avg function.
---

# avg

Get the average of the values in a group

## Signature

> AVG(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select AVG(hits) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 3692601 | 
