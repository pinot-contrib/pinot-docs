---
description: >-
  This section contains reference documentation for the byteswapInt function.
---

# byteswapInt

Reverses the byte order of an integer value. Useful for converting between big-endian and little-endian representations.

## Signature

> byteswapInt(col)

| Argument | Type | Description              |
| -------- | ---- | ------------------------ |
| `col`    | INT  | Integer value to reverse |

Returns: **INT**

## Usage Examples

```sql
SELECT byteswapInt(intCol) AS value
FROM myTable
```
