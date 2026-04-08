---
description: >-
  This section contains reference documentation for the positiveModulo function.
---

# positiveModulo

Returns the modulo of two values, always returning a non-negative result. If the standard modulo result is negative, it adds the absolute value of the divisor to produce a positive result.

## Signature

> positiveModulo(col1, col2)

| Argument | Type   | Description |
| -------- | ------ | ----------- |
| `col1`   | DOUBLE | Dividend    |
| `col2`   | DOUBLE | Divisor     |

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT positiveModulo(10, 3) AS value
FROM myTable
```

| value |
| ----- |
| 1.0   |

```sql
SELECT positiveModulo(-7, 3) AS value
FROM myTable
```

| value |
| ----- |
| 2.0   |
