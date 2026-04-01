---
description: This section contains reference documentation for the rtrim function.
---

# rtrim

rtrim spaces from right side of the string

## Signature

> RTRIM(col)

## Usage Examples

```sql
SELECT ' Pinot with spaces  ' AS notTrimmed,
       rtrim(' Pinot with spaces ') AS trimmed
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
      <td>`" Pinot with spaces"`</td>
    </tr>
  </tbody>
</table>
