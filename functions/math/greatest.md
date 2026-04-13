---
description: This section contains reference documentation for the greatest function.
---

# GREATEST

Returns the larger of two or more values. This is a polymorphic function that preserves the input numeric type.

## Signature

GREATEST(col1, col2, ...)

| Argument | Type                                    | Description       |
| -------- | --------------------------------------- | ------------------|
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | First value       |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Second value      |
| `...`    | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Additional values |

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
select GREATEST(10, 5) AS value
from ignoreMe
```

| value |
| ----- |
| 10    |

```sql
select GREATEST(100, 50, 75) AS value
from ignoreMe
```

| value |
| ----- |
| 100   |

```sql
select GREATEST(42, 100L) AS greatest_int_long, GREATEST(3.14F, 2.71F) AS float_greatest, GREATEST(2.718, 3.14159) AS double_greatest
from myTable
```

Returns LONG, FLOAT, DOUBLE respectively (preserving input type).