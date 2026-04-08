---
description: >-
  This section contains reference documentation for the moduloOrZero function.
---

# moduloOrZero

Same as [MOD](mod.md) but returns zero when dividing by zero or when dividing `Long.MIN_VALUE` by `-1`.

## Signature

> moduloOrZero(col1, col2)

| Argument | Type   | Description |
| -------- | ------ | ----------- |
| `col1`   | DOUBLE | Dividend    |
| `col2`   | DOUBLE | Divisor     |

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT moduloOrZero(10, 3) AS value
FROM myTable
```

| value |
| ----- |
| 1.0   |

```sql
SELECT moduloOrZero(10, 0) AS value
FROM myTable
```

| value |
| ----- |
| 0.0   |
