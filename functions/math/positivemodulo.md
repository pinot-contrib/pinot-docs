---
description: >-
  This section contains reference documentation for the positiveModulo function.
---

# positiveModulo

Returns the modulo of two values, always returning a non-negative result. If the standard modulo result is negative, it adds the absolute value of the divisor to produce a positive result. This is a polymorphic function that preserves the input numeric type.

## Signature

positiveModulo(col1, col2)

| Argument | Type                                    | Description |
| -------- | --------------------------------------- | ----------- |
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Dividend    |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Divisor     |

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
SELECT positiveModulo(10, 3) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT positiveModulo(-7, 3) AS value
FROM myTable
```

| value |
| ----- |
| 2     |

```sql
SELECT positiveModulo(10L, 3L) AS long_modulo, positiveModulo(-7.5F, 3.0F) AS float_modulo, positiveModulo(-7.5, 3.0) AS double_modulo
FROM myTable
```

Returns LONG, FLOAT, DOUBLE respectively (preserving input type).