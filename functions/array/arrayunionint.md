---
description: This section contains reference documentation for the arrayUnionInt function.
---

# arrayUnionInt

Create a union of two arrays of ints.

## Signature

> arrayUnionInt('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivWheelsOffs, 
       DivWheelsOns,
       arrayUnionInt(DivWheelsOffs, DivWheelsOns) AS unionIds
from airlineStats 
WHERE arraylength(DivWheelsOffs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivWheelsOffs</th>
      <th>DivWheelsOns</th>
      <th>unionIds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1453,1731</td>
      <td>1415,1623</td>
      <td>1453,1731,1415,1623</td>
    </tr>
    <tr>
      <td>1908,1758</td>
      <td>1339,2310</td>
      <td>1908,1758,1339,2310</td>
    </tr>
    <tr>
      <td>1453,1731</td>
      <td>1415,1623</td>
      <td>1453,1731,1415,1623</td>
    </tr>
    <tr>
      <td>1908,1758</td>
      <td>1339,2310</td>
      <td>1908,1758,1339,2310</td>
    </tr>
  </tbody>
</table>
