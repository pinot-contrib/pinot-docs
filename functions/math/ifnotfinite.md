---
description: >-
  This section contains reference documentation for the ifNotFinite function.
---

# ifNotFinite

Returns the input value if it is finite, otherwise returns the specified default value. Useful for replacing infinite or NaN values with a fallback.

## Signature

> ifNotFinite(valueToCheck, defaultValue)

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`valueToCheck`</td>
      <td>DOUBLE</td>
      <td>Value to check for finiteness</td>
    </tr>
    <tr>
      <td>`defaultValue`</td>
      <td>DOUBLE</td>
      <td>Value to return if `valueToCheck` is not finite</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>-1.0</td>
    </tr>
  </tbody>
</table>

```sql
SELECT ifNotFinite(42.5, -1) AS value
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>42.5</td>
    </tr>
  </tbody>
</table>
