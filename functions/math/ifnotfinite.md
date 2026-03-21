---
description: >-
  This section contains reference documentation for the ifNotFinite function.
---

# ifNotFinite

Returns the input value if it is finite, otherwise returns the specified default value. Useful for replacing infinite or NaN values with a fallback.

## Signature

> ifNotFinite(valueToCheck, defaultValue)

| Argument        | Type   | Description                                  |
| --------------- | ------ | -------------------------------------------- |
| `valueToCheck`  | DOUBLE | Value to check for finiteness                |
| `defaultValue`  | DOUBLE | Value to return if `valueToCheck` is not finite |

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT ifNotFinite(ratio, 0) AS value
FROM myTable
```

Returns `ratio` if it is finite, otherwise returns `0`.

```sql
SELECT ifNotFinite(1.0 / 0.0, -1) AS value
FROM myTable
```

| value |
| ----- |
| -1.0  |

```sql
SELECT ifNotFinite(42.5, -1) AS value
FROM myTable
```

| value |
| ----- |
| 42.5  |
