---
description: >-
  This section contains reference documentation for the negate function.
---

# negate

Returns the negation of the input value. This is a polymorphic function that preserves the input numeric type.

## Signature

negate(col)

| Argument | Type                                    | Description     |
| -------- | --------------------------------------- | ---------------- |
| `col`    | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Value to negate  |

Returns the same type as the input argument.

## Usage Examples

```sql
SELECT negate(42.5) AS value
FROM myTable
```

| value  |
| ------ |
| -42.5  |

```sql
SELECT negate(-10) AS value
FROM myTable
```

| value |
| ----- |
| 10    |

```sql
SELECT negate(100) AS int_neg, negate(1000000L) AS long_neg, negate(3.14F) AS float_neg, negate(2.718) AS double_neg
FROM myTable
```

Returns INT, LONG, FLOAT, DOUBLE respectively (preserving input type).