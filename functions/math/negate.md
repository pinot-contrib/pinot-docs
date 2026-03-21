---
description: >-
  This section contains reference documentation for the negate function.
---

# negate

Returns the negation of the input value.

## Signature

> negate(col)

| Argument | Type   | Description      |
| -------- | ------ | ---------------- |
| `col`    | DOUBLE | Value to negate  |

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT negate(42.5) AS value
FROM myTable
```

| value  |
| ------ |
| -42.5  |

```sql
SELECT negate(-10) AS value
FROM myTable
```

| value |
| ----- |
| 10.0  |
