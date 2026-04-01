---
description: >-
  This section contains reference documentation for the gcd function.
---

# gcd

Returns the greatest common divisor of two long values.

## Signature

> gcd(col1, col2)

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
      <td>LONG</td>
      <td>First value</td>
    </tr>
    <tr>
      <td>`col2`</td>
      <td>LONG</td>
      <td>Second value</td>
    </tr>
  </tbody>
</table>

Returns: **LONG**

## Usage Examples

```sql
SELECT gcd(12, 8) AS value
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
      <td>4</td>
    </tr>
  </tbody>
</table>

```sql
SELECT gcd(0, 5) AS value
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
      <td>5</td>
    </tr>
  </tbody>
</table>
