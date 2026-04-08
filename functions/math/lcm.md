---
description: >-
  This section contains reference documentation for the lcm function.
---

# lcm

Returns the least common multiple of two long values. Returns `0` if either input is `0`.

## Signature

> lcm(col1, col2)

| Argument | Type | Description  |
| -------- | ---- | ------------ |
| `col1`   | LONG | First value  |
| `col2`   | LONG | Second value |

Returns: **LONG**

## Usage Examples

```sql
SELECT lcm(4, 6) AS value
FROM myTable
```

| value |
| ----- |
| 12    |

```sql
SELECT lcm(0, 5) AS value
FROM myTable
```

| value |
| ----- |
| 0     |
