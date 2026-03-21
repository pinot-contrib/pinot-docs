---
description: >-
  This section contains reference documentation for the byteswapLong function.
---

# byteswapLong

Reverses the byte order of a long value. Useful for converting between big-endian and little-endian representations.

## Signature

> byteswapLong(col)

| Argument | Type | Description           |
| -------- | ---- | --------------------- |
| `col`    | LONG | Long value to reverse |

Returns: **LONG**

## Usage Examples

```sql
SELECT byteswapLong(longCol) AS value
FROM myTable
```
