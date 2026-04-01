---
description: This section contains reference documentation for the SUMMV function.
---

# summv

Get the sum of values in a group

## Signature

> SUMMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select SUMMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2696</td>
    </tr>
  </tbody>
</table>
