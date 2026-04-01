---
description: This section contains reference documentation for the BOOLOR function.
---

# BOOLOR

Returns the logical OR of all boolean values in a group. Returns `true` if any value in the group is `true`; returns `false` only if every value is `false`. When no records are selected, the default value is `false` (the identity element for OR).

## Signature

> BOOLOR(colName)

## Usage Examples

```sql
select BOOLOR(hasError) AS value
from myTable
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>true</td>
    </tr>
  </tbody>
</table>

```sql
select city, BOOLOR(hasError) AS anyErrors
from myTable
GROUP BY city
```

<table>
  <thead>
    <tr>
      <th>city</th>
      <th>anyErrors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>San Francisco</td>
      <td>true</td>
    </tr>
    <tr>
      <td>New York</td>
      <td>false</td>
    </tr>
  </tbody>
</table>
