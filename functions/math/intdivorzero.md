---
description: >-
  This section contains reference documentation for the intDivOrZero function.
---

# intDivOrZero

Same as [intDiv](intdiv.md) but returns zero when dividing by zero or when dividing `Long.MIN_VALUE` by `-1`.

## Signature

> intDivOrZero(col1, col2)

| Argument | Type   | Description |
| -------- | ------ | ----------- |
| `col1`   | DOUBLE | Dividend    |
| `col2`   | DOUBLE | Divisor     |

Returns: **LONG**

## Usage Examples

```sql
SELECT intDivOrZero(10, 3) AS value
FROM myTable
```

| value |
| ----- |
| 3     |

```sql
SELECT intDivOrZero(10, 0) AS value
FROM myTable
```

| value |
| ----- |
| 0     |
