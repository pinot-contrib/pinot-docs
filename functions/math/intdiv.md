---
description: >-
  This section contains reference documentation for the intDiv function.
---

# intDiv

Returns the integer result of dividing the first argument by the second, rounded down (floor division).

## Signature

> intDiv(col1, col2)

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
SELECT intDiv(10, 3) AS value
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
SELECT intDiv(7.5, 2) AS value
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

{% hint style="info" %}
If dividing by zero, this function does not return zero. Use [intDivOrZero](intdivorzero.md) for safe division that returns zero on division by zero.
{% endhint %}
