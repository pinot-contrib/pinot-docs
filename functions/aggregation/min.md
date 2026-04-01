---
description: This section contains reference documentation for the min function.
---

# min

Get the minimum value in a group

## Signature

> MIN(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select min(yearID) AS value
from baseballStats 
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1871</td>
    </tr>
  </tbody>
</table>
