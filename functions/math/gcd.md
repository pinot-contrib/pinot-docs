---
description: >-
  This section contains reference documentation for the gcd function.
---

# gcd

Returns the greatest common divisor of two long values.

## Signature

> gcd(col1, col2)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `col1`   | LONG | First value |
| `col2`   | LONG | Second value |

Returns: **LONG**

## Usage Examples

```sql
SELECT gcd(12, 8) AS value
FROM myTable
```

| value |
| ----- |
| 4     |

```sql
SELECT gcd(0, 5) AS value
FROM myTable
```

| value |
| ----- |
| 5     |
