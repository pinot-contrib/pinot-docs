---
description: This section contains reference documentation for the minmaxrange function.
---

# MINMAXRANGE

Returns the `max` - `min` value in a group

## Signature

> MINMAXRANGE(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select MINMAXRANGE(yearID) AS value
from baseballStats 
```

| value |
| ----- |
| 142   |
