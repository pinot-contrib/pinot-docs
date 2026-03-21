---
description: >-
  This section contains reference documentation for the intDiv function.
---

# intDiv

Returns the integer result of dividing the first argument by the second, rounded down (floor division).

## Signature

> intDiv(col1, col2)

| Argument | Type   | Description |
| -------- | ------ | ----------- |
| `col1`   | DOUBLE | Dividend    |
| `col2`   | DOUBLE | Divisor     |

Returns: **LONG**

## Usage Examples

```sql
SELECT intDiv(10, 3) AS value
FROM myTable
```

| value |
| ----- |
| 3     |

```sql
SELECT intDiv(7.5, 2) AS value
FROM myTable
```

| value |
| ----- |
| 3     |

{% hint style="info" %}
If dividing by zero, this function does not return zero. Use [intDivOrZero](intdivorzero.md) for safe division that returns zero on division by zero.
{% endhint %}
