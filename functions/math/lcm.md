---
description: >-
  This section contains reference documentation for the lcm function.
---

# lcm

Returns the least common multiple of two long values. Returns `0` if either input is `0`.

## Signature

> lcm(col1, col2)

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
SELECT lcm(4, 6) AS value
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
      <td>12</td>
    </tr>
  </tbody>
</table>

```sql
SELECT lcm(0, 5) AS value
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
