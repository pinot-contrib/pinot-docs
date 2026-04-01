---
description: This section contains reference documentation for the FLOOR function.
---

# FLOOR

Rounded down to the nearest integer.

## Signature

> FLOOR(col1)

## Usage Examples

```sql
select FLOOR(12.1) AS value
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
      <td>12</td>
    </tr>
  </tbody>
</table>

```sql
select FLOOR(-12.1) AS value
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
      <td>-13</td>
    </tr>
  </tbody>
</table>
