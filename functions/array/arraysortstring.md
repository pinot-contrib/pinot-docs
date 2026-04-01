---
description: >-
  This section contains reference documentation for the arraySortString
  function.
---

# arraySortString

Sorts array of strings.

## Signature

> arraySortString('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arraySortString(RandomAirports) AS sortedAirports, 
       RandomAirports
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

<table>
  <thead>
    <tr>
      <th>FlightNum</th>
      <th>sortedAirports</th>
      <th>RandomAirports</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>3846</td>
      <td>PSC,SEA</td>
      <td>SEA,PSC</td>
    </tr>
    <tr>
      <td>3635</td>
      <td>MSY,PHX,PSC,SEA</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>429</td>
      <td>MSY,PHX,PSC,SEA</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>1206</td>
      <td>PSC,SEA</td>
      <td>SEA,PSC</td>
    </tr>
    <tr>
      <td>5300</td>
      <td>PSC,SEA</td>
      <td>SEA,PSC</td>
    </tr>
  </tbody>
</table>
