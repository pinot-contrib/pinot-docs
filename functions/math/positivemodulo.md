---
description: >-
  This section contains reference documentation for the positiveModulo function.
---

# positiveModulo

Returns the modulo of two values, always returning a non-negative result. If the standard modulo result is negative, it adds the absolute value of the divisor to produce a positive result.

## Signature

> positiveModulo(col1, col2)

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
SELECT positiveModulo(10, 3) AS value
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
SELECT positiveModulo(-7, 3) AS value
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
      <td>2.0</td>
    </tr>
  </tbody>
</table>
