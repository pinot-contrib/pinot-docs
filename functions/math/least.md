---
description: This section contains reference documentation for the least function.
---

# LEAST

Returns the smaller of two or more values. This is a polymorphic function that preserves the input numeric type.

## Signature

LEAST(col1, col2, ...)

| Argument | Type                                    | Description       |
| -------- | --------------------------------------- | ------------------|
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | First value       |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Second value      |
| `...`    | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Additional values |

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
select LEAST(10, 5) AS value
from ignoreMe
```

| value |
| ----- |
| 5     |

```sql
select LEAST(100, 50, 75) AS value
from ignoreMe
```

| value |
| ----- |
| 50    |

```sql
select LEAST(42, 100L) AS least_int_long, LEAST(3.14F, 2.71F) AS float_least, LEAST(2.718, 3.14159) AS double_least
from myTable
```

Returns LONG, FLOAT, DOUBLE respectively (preserving input type).