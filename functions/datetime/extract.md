---
description: This section contains reference documentation for the Extract function.
---

# Extract

Returns the selected field from the DATETIME expression.

### Signature

> EXTRACT(field FROM expression)

### Usage Examples

```sql
select EXTRACT(MONTH FROM '2017-06-15')
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>06</td>
    </tr>
  </tbody>
</table>

```sql
select EXTRACT(YEAR FROM '2017-06-15 09:34:21')
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2017</td>
    </tr>
  </tbody>
</table>
