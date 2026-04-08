---
description: >-
  This section contains reference documentation for the isNaN function.
---

# isNaN

Returns `1` if the value is NaN (Not a Number), `0` otherwise.

## Signature

> isNaN(col)

| Argument | Type   | Description      |
| -------- | ------ | ---------------- |
| `col`    | DOUBLE | Value to check   |

Returns: **INT** (`1` or `0`)

## Usage Examples

```sql
SELECT isNaN(0.0 / 0.0) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT isNaN(100.5) AS value
FROM myTable
```

| value |
| ----- |
| 0     |
