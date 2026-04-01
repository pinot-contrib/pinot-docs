---
description: >-
  This section contains reference documentation for the arraySliceString
  function.
---

# arraySliceString

Returns the values in the array between the start and end positions.

## Signature

> arraySliceString('colName', start, end)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arraySliceString(RandomAirports, 0, 2) AS airports, 
       RandomAirports
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

<table>
  <thead>
    <tr>
      <th>FlightNum</th>
      <th>airports</th>
      <th>RandomAirports</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>671</td>
      <td>SEA,PSC</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>1767</td>
      <td>SEA,PSC</td>
      <td>SEA,PSC,PHX</td>
    </tr>
    <tr>
      <td>2522</td>
      <td>SEA,PSC</td>
      <td>SEA,PSC</td>
    </tr>
    <tr>
      <td>424</td>
      <td>SEA,PSC</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>3162</td>
      <td>SEA,PSC</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
  </tbody>
</table>
