---
description: >-
  This section contains reference documentation for the arrayPushFront
  functions.
---

# arrayPushFront

Prepends one element to the beginning of an array.

## Supported Variants

| Function | Signature | Return Type |
| --- | --- | --- |
| `arrayPushFrontInt` | `arrayPushFrontInt(values, element)` | `INT[]` |
| `arrayPushFrontLong` | `arrayPushFrontLong(values, element)` | `LONG[]` |
| `arrayPushFrontFloat` | `arrayPushFrontFloat(values, element)` | `FLOAT[]` |
| `arrayPushFrontDouble` | `arrayPushFrontDouble(values, element)` | `DOUBLE[]` |
| `arrayPushFrontString` | `arrayPushFrontString(values, element)` | `STRING[]` |

## Usage Examples

These examples are based on the inputs used in Pinot's array function tests.

```sql
SELECT arrayPushFrontInt(intArray, 7) AS updatedArray
FROM myTable
```

Returns `[7, 3, 2, 10, 6, 1, 12]` when `intArray` is `[3, 2, 10, 6, 1, 12]`.

```sql
SELECT arrayPushFrontString(stringArray, 'x') AS updatedArray
FROM myTable
```

Returns `['x', '3', '2', '10', '6', '1', '12']` when `stringArray` is `['3', '2', '10', '6', '1', '12']`.
