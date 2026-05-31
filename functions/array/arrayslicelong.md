---
description: This section contains reference documentation for the arraySliceLong function.
---

# arraySliceLong

Returns the LONG values in the array between the start and end positions. The `start` index is inclusive and the `end` index is exclusive.

## Signature

> arraySliceLong('colName', start, end)

## Usage Examples

This example uses a LONG array literal.

```sql
select arraySliceLong(ARRAY[10000000000, 20000000000, 30000000000, 40000000000], 1, 3) AS slice
```

| slice                 |
| --------------------- |
| 20000000000,30000000000 |
