---
description: >-
  This section contains reference documentation for the arrayReverseString
  function.
---

# arrayReverseString

Reverses array of strings.

## Signature

> arrayReverseString('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arrayReverseString(RandomAirports) AS reversedAirports, 
       RandomAirports
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

<table>
  <thead>
    <tr>
      <th>FlightNum</th>
      <th>reversedAirports</th>
      <th>RandomAirports</th>
    </tr>
  </thead>
  <tbody>
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
    <tr>
      <td>3359</td>
      <td>MSY,PHX,PSC,SEA</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>1023</td>
      <td>PHX,PSC,SEA</td>
      <td>SEA,PSC,PHX</td>
    </tr>
    <tr>
      <td>963</td>
      <td>MSY,PHX,PSC,SEA</td>
      <td>SEA,PSC,PHX,MSY</td>
    </tr>
  </tbody>
</table>
