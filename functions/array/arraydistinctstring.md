---
description: >-
  This section contains reference documentation for the arrayDistinctString
  function.
---

# arrayDistinctString

Returns unique values in an array of strings.

## Signature

> arrayDistinctString('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivTailNums, 
       arrayDistinctString(DivTailNums) AS unique
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivTailNums</th>
      <th>unique</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>N7713A,N7713A</td>
      <td>N7713A</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
      <td>N344AA</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
      <td>N344AA</td>
    </tr>
    <tr>
      <td>N7713A,N7713A</td>
      <td>N7713A</td>
    </tr>
  </tbody>
</table>
