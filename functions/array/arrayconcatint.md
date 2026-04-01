---
description: This section contains reference documentation for the arrayConcatInt function.
---

# arrayConcatInt

Concatenates two arrays of ints.

## Signature

> arrayConcatInt('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivWheelsOffs, 
       arrayConcatInt(DivWheelsOffs, DivWheelsOns) AS concatIds
from airlineStats 
WHERE arraylength(DivWheelsOffs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivWheelsOffs</th>
      <th>concatIds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1453,1731</td>
      <td>1453,1731,1415,1623</td>
    </tr>
    <tr>
      <td>1908,1758</td>
      <td>1908,1758,1339,2310</td>
    </tr>
    <tr>
      <td>1453,1731</td>
      <td>1453,1731,1415,1623</td>
    </tr>
    <tr>
      <td>1908,1758</td>
      <td>1908,1758,1339,2310</td>
    </tr>
  </tbody>
</table>
