---
description: This section contains reference documentation for the concat function.
---

# concat

Concatenate two input strings using the seperator

## Signature

> CONCAT(col1, col2, seperator)

## Usage Examples

```sql
SELECT concat('Apache', 'Pinot', ' ') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Apache Pinot</td>
    </tr>
  </tbody>
</table>

```sql
SELECT concat('real-time', 'analytics', '__') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>real-time\_\_analytics</td>
    </tr>
  </tbody>
</table>
