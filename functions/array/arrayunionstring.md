---
description: >-
  This section contains reference documentation for the arrayUnionString
  function.
---

# arrayUnionString

Create a union of two arrays of strings.

## Signature

> arrayUnionString('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivTailNums, 
       DivAirports,
       arrayUnionString(DivTailNums, DivAirports) AS unionIds
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivTailNums</th>
      <th>DivAirports</th>
      <th>unionIds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>N7713A,N7713A</td>
      <td>IND,IND</td>
      <td>N7713A,IND</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
      <td>MCI,BOS</td>
      <td>N344AA,MCI,BOS</td>
    </tr>
    <tr>
      <td>N7713A,N7713A</td>
      <td>IND,IND</td>
      <td>N7713A,IND</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
      <td>MCI,BOS</td>
      <td>N344AA,MCI,BOS</td>
    </tr>
  </tbody>
</table>
