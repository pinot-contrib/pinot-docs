---
description: >-
  This section contains reference documentation for the intDivOrZero function.
---

# intDivOrZero

Same as [intDiv](intdiv.md) but returns zero when dividing by zero or when dividing `Long.MIN_VALUE` by `-1`.

## Signature

> intDivOrZero(col1, col2)

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

Returns: **LONG**

## Usage Examples

```sql
SELECT intDivOrZero(10, 3) AS value
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
      <td>3</td>
    </tr>
  </tbody>
</table>

```sql
SELECT intDivOrZero(10, 0) AS value
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
