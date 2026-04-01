---
description: This section contains reference documentation for the ltrim function.
---

# ltrim

trim spaces from left side of the string

## Signature

> LTRIM(col)

## Usage Examples

```sql
SELECT ' Pinot with spaces  ' AS notTrimmed,
       ltrim(' Pinot with spaces ') AS trimmed
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>notTrimmed</th>
      <th>trimmed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`" Pinot with spaces "`</td>
      <td>`"Pinot with spaces "`</td>
    </tr>
  </tbody>
</table>
