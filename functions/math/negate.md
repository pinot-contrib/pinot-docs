---
description: >-
  This section contains reference documentation for the negate function.
---

# negate

Returns the negation of the input value.

## Signature

> negate(col)

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
      <td>Value to negate</td>
    </tr>
  </tbody>
</table>

Returns: **DOUBLE**

## Usage Examples

```sql
SELECT negate(42.5) AS value
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
      <td>-42.5</td>
    </tr>
  </tbody>
</table>

```sql
SELECT negate(-10) AS value
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
      <td>10.0</td>
    </tr>
  </tbody>
</table>
