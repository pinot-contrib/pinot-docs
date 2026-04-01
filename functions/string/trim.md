---
description: This section contains reference documentation for the trim function.
---

# trim

trim spaces from both side of the string

## Signature

> TRIM(col)

## Usage Examples

```sql
SELECT ' Pinot with spaces  ' AS notTrimmed,
       trim(' Pinot with spaces ') AS trimmed
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
      <td>`"Pinot with spaces"`</td>
    </tr>
  </tbody>
</table>
