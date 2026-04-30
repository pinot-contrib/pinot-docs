---
description: >-
  This section contains reference documentation for the arraysOverlap
  function.
---

# arraysOverlap

Returns `true` when two arrays of the same element type share at least one value.

## Signature

> ARRAYS_OVERLAP(array1, array2)

Pinot also accepts `ARRAYSOVERLAP`.

## Supported Types

| Array Type | Return Type |
| --- | --- |
| `INT[]` | `BOOLEAN` |
| `LONG[]` | `BOOLEAN` |
| `FLOAT[]` | `BOOLEAN` |
| `DOUBLE[]` | `BOOLEAN` |
| `BIG_DECIMAL[]` | `BOOLEAN` |
| `STRING[]` | `BOOLEAN` |
| `BYTES[]` | `BOOLEAN` |

Both arguments must have the same array type.

## Usage Examples

These examples are derived from Pinot's integration tests.

```sql
SELECT ARRAYS_OVERLAP(ARRAY[1, 2], ARRAY[3, 2]) AS hasOverlap
```

Returns `true`.

```sql
SELECT ARRAYS_OVERLAP(ARRAY['a', 'b'], ARRAY['x', 'y']) AS hasOverlap
```

Returns `false`.

```sql
SELECT COUNT(*)
FROM myTable
WHERE ARRAYS_OVERLAP(longArrayCol, ARRAY[CAST(2 AS BIGINT), CAST(10 AS BIGINT)])
```

Returns all rows where `longArrayCol` shares at least one value with the filter array.
