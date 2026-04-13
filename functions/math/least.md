---
description: >-
  This section contains reference documentation for the least function.
---

# least

Returns the smaller of two values. This is a polymorphic function that preserves the input numeric type.

## Signature

least(col1, col2)

| Argument | Type                                    | Description |
| -------- | --------------------------------------- | ----------- |
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | First value |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Second value|

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
SELECT least(10, 5) AS value
FROM myTable
```

| value |
| ----- |
| 5     |

```sql
SELECT least(10.5, 10.3) AS value
FROM myTable
```

| value |
| ----- |
| 10.3  |

```sql
SELECT least(100, 50L) AS mixed_int_long, least(3.14F, 2.71F) AS float_least, least(3.14, 2.71) AS double_least
FROM myTable
```

Returns INT/LONG, FLOAT, DOUBLE respectively (preserving input type or the wider type).