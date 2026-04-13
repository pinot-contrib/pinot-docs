---
description: This section contains reference documentation for the abs function.
---

# ABS

Absolute value of a number. This is a polymorphic function that preserves the input numeric type.

## Signature

ABS(col1)

| Argument | Type                                    | Description           |
| -------- | --------------------------------------- | --------------------- |
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Value to get absolute |

Returns the same type as the input argument.

## Usage Examples

```sql
select ABS(-12.1) AS value
from ignoreMe
```

| value |
| ----- |
| 12.1  |

```sql
select ABS(12.1) AS value
from ignoreMe
```

| value |
| ----- |
| 12.1  |

```sql
select ABS(-42) AS int_abs, ABS(-1000000L) AS long_abs, ABS(-3.14F) AS float_abs, ABS(-2.718) AS double_abs
from myTable
```

Returns INT, LONG, FLOAT, DOUBLE respectively (preserving input type).