---
description: >-
  This section contains reference documentation for the isFinite function.
---

# isFinite

Returns `1` if the value is finite (not infinite and not NaN), `0` otherwise.

## Signature

> isFinite(col)

| Argument | Type   | Description      |
| -------- | ------ | ---------------- |
| `col`    | DOUBLE | Value to check   |

Returns: **INT** (`1` or `0`)

## Usage Examples

```sql
SELECT isFinite(100.5) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT isFinite(1.0 / 0.0) AS value
FROM myTable
```

| value |
| ----- |
| 0     |

{% hint style="info" %}
See also [isInfinite](isinfinite.md), [isNaN](isnan.md), and [ifNotFinite](ifnotfinite.md).
{% endhint %}
