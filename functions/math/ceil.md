---
description: This section contains reference documentation for the CEIL function.
---

# ceil

Rounded up to the nearest integer.

## Signature

> CEIL(col1)

## Usage Examples

```sql
select CEIL(12.1) AS value
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
      <td>13</td>
    </tr>
  </tbody>
</table>

```sql
select CEIL(-12.1) AS value
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
      <td>-12</td>
    </tr>
  </tbody>
</table>
