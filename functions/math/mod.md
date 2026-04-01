---
description: This section contains reference documentation for the MOD function.
---

# MOD

Modulo of two values

## Signature

> MOD(col1, col2)

## Usage Examples

```sql
select MOD(12, 5) AS value
from ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2</td>
    </tr>
  </tbody>
</table>

```sql
select MOD(12, 2) AS value
from ignoreMe
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
