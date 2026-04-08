---
description: >-
  This section contains reference documentation for the arrayPushBack
  functions.
---

# arrayPushBack

Appends one element to the end of an array.

## Supported Variants

| Function | Signature | Return Type |
| --- | --- | --- |
| `arrayPushBackInt` | `arrayPushBackInt(values, element)` | `INT[]` |
| `arrayPushBackLong` | `arrayPushBackLong(values, element)` | `LONG[]` |
| `arrayPushBackFloat` | `arrayPushBackFloat(values, element)` | `FLOAT[]` |
| `arrayPushBackDouble` | `arrayPushBackDouble(values, element)` | `DOUBLE[]` |
| `arrayPushBackString` | `arrayPushBackString(values, element)` | `STRING[]` |

## Usage Examples

These examples are based on the inputs used in Pinot's array function tests.

```sql
SELECT arrayPushBackInt(intArray, 7) AS updatedArray
FROM myTable
```

Returns `[3, 2, 10, 6, 1, 12, 7]` when `intArray` is `[3, 2, 10, 6, 1, 12]`.

```sql
SELECT arrayPushBackString(stringArray, 'x') AS updatedArray
FROM myTable
```

Returns `['3', '2', '10', '6', '1', '12', 'x']` when `stringArray` is `['3', '2', '10', '6', '1', '12']`.
