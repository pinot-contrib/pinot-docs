---
description: This section contains reference documentation for the minString function.
---

# minString

Get the minimum string value lexicographically from a string column

## Signature

> MINSTRING(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select MINSTRING(playerName) as minString from baseballStats
```

<table>
  <thead>
    <tr>
      <th>minString</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A. Harry</td>
    </tr>
  </tbody>
</table>
