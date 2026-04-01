---
description: This section contains reference documentation for the max function.
---

# max

Get the maximum value in a group

## Signature

> MAX(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select max(homeRuns) AS value
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
      <td>73</td>
    </tr>
  </tbody>
</table>
