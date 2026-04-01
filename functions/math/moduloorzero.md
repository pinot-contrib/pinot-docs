---
description: >-
  This section contains reference documentation for the moduloOrZero function.
---

# moduloOrZero

Same as [MOD](mod.md) but returns zero when dividing by zero or when dividing `Long.MIN_VALUE` by `-1`.

## Signature

> moduloOrZero(col1, col2)

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
      <td>`col1`</td>
      <td>DOUBLE</td>
      <td>Dividend</td>
    </tr>
    <tr>
      <td>`col2`</td>
      <td>DOUBLE</td>
      <td>Divisor</td>
    </tr>
  </tbody>
</table>

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT moduloOrZero(10, 3) AS value
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
      <td>1.0</td>
    </tr>
  </tbody>
</table>

```sql
SELECT moduloOrZero(10, 0) AS value
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
      <td>0.0</td>
    </tr>
  </tbody>
</table>
