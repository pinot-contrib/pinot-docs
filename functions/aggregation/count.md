---
description: This section contains reference documentation for the count function.
---

# count

Get the count of rows in a group

## Signature

> COUNT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select count(*) AS value
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
      <td>97889</td>
    </tr>
  </tbody>
</table>
