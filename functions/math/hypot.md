---
description: >-
  This section contains reference documentation for the hypot function.
---

# hypot

Returns the hypotenuse of a right-angled triangle, computed as `sqrt(col1² + col2²)`, without intermediate overflow or underflow.

## Signature

> hypot(col1, col2)

| Argument | Type   | Description                 |
| -------- | ------ | --------------------------- |
| `col1`   | DOUBLE | Length of one side           |
| `col2`   | DOUBLE | Length of the other side     |

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT hypot(3, 4) AS value
FROM myTable
```

| value |
| ----- |
| 5.0   |

```sql
SELECT hypot(5, 12) AS value
FROM myTable
```

| value |
| ----- |
| 13.0  |
