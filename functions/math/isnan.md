---
description: >-
  This section contains reference documentation for the isNaN function.
---

# isNaN

Returns `1` if the value is NaN (Not a Number), `0` otherwise.

## Signature

> isNaN(col)

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
      <td>`col`</td>
      <td>DOUBLE</td>
      <td>Value to check</td>
    </tr>
  </tbody>
</table>

Returns: **INT** (`1` or `0`)

## Usage Examples

```sql
SELECT isNaN(0.0 / 0.0) AS value
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
      <td>1</td>
    </tr>
  </tbody>
</table>

```sql
SELECT isNaN(100.5) AS value
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
      <td>0</td>
    </tr>
  </tbody>
</table>
