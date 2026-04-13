---
description: This section contains reference documentation for the MOD function.
---

# MOD

Modulo (remainder) of two values. This is a polymorphic function that preserves the input numeric type.

## Signature

MOD(col1, col2)

| Argument | Type                                    | Description |
| -------- | --------------------------------------- | ----------- |
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Dividend    |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Divisor     |

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
select MOD(12, 5) AS value
from ignoreMe
```

| value |
| ----- |
| 2     |

```sql
select MOD(12, 2) AS value
from ignoreMe
```

| value |
| ----- |
| 0     |

```sql
select MOD(12L, 5) AS long_mod, MOD(12.5F, 5.0F) AS float_mod, MOD(12.5, 5.0) AS double_mod
from myTable
```

Returns LONG, FLOAT, DOUBLE respectively (preserving input type).