---
description: >-
  This section contains reference documentation for the greatest function.
---

# greatest

Returns the larger of two values. This is a polymorphic function that preserves the input numeric type.

## Signature

greatest(col1, col2)

| Argument | Type                                    | Description |
| -------- | --------------------------------------- | ----------- |
| `col1`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | First value |
| `col2`   | INT, LONG, FLOAT, DOUBLE, BIG_DECIMAL  | Second value|

Returns the same numeric type as the inputs (or the wider type if inputs differ).

## Usage Examples

```sql
SELECT greatest(10, 5) AS value
FROM myTable
```

| value |
| ----- |
| 10    |

```sql
SELECT greatest(10.5, 10.3) AS value
FROM myTable
```

| value |
| ----- |
| 10.5  |

```sql
SELECT greatest(100, 50L) AS mixed_int_long, greatest(3.14F, 2.71F) AS float_greatest, greatest(3.14, 2.71) AS double_greatest
FROM myTable
```

Returns INT/LONG, FLOAT, DOUBLE respectively (preserving input type or the wider type).