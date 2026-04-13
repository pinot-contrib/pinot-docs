---
description: >-
  This section contains reference documentation for the moduloOrZero function.
---

# moduloOrZero

Same as [MOD](mod.md) but returns zero when dividing by zero or when dividing `Long.MIN_VALUE` by `-1`. This is a polymorphic function that preserves the input numeric type.

## Signature

moduloOrZero(col1, col2)

| Argument | Type                                    | Description |
| -------- | --------------------------------------- | ----------- |
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Dividend    |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Divisor     |

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
SELECT moduloOrZero(10, 3) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT moduloOrZero(10, 0) AS value
FROM myTable
```

| value |
| ----- |
| 0     |

```sql
SELECT moduloOrZero(10L, 3L) AS long_modulo, moduloOrZero(10.5F, 3.0F) AS float_modulo, moduloOrZero(10.5, 3.0) AS double_modulo
FROM myTable
```

Returns LONG, FLOAT, DOUBLE respectively (preserving input type).