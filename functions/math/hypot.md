---
description: >-
  This section contains reference documentation for the hypot function.
---

# hypot

Returns the hypotenuse of a right-angled triangle, computed as `sqrt(col1² + col2²)`, without intermediate overflow or underflow.

## Signature

> hypot(col1, col2)

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
      <td>Length of one side</td>
    </tr>
    <tr>
      <td>`col2`</td>
      <td>DOUBLE</td>
      <td>Length of the other side</td>
    </tr>
  </tbody>
</table>

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT hypot(3, 4) AS value
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
      <td>5.0</td>
    </tr>
  </tbody>
</table>

```sql
SELECT hypot(5, 12) AS value
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
      <td>13.0</td>
    </tr>
  </tbody>
</table>
