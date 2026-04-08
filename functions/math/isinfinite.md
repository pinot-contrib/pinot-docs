---
description: >-
  This section contains reference documentation for the isInfinite function.
---

# isInfinite

Returns `1` if the value is infinite (positive or negative infinity), `0` otherwise.

## Signature

> isInfinite(col)

| Argument | Type   | Description      |
| -------- | ------ | ---------------- |
| `col`    | DOUBLE | Value to check   |

Returns: **INT** (`1` or `0`)

## Usage Examples

```sql
SELECT isInfinite(1.0 / 0.0) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT isInfinite(100.5) AS value
FROM myTable
```

| value |
| ----- |
| 0     |
