---
description: This section contains reference documentation for the minmaxrange function.
---

# minmaxrange

Returns the `max` - `min` value in a group

## Signature

> MINMAXRANGE(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select MINMAXRANGE(yearID) AS value
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
      <td>142</td>
    </tr>
  </tbody>
</table>
