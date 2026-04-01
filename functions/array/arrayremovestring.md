---
description: >-
  This section contains reference documentation for the arrayRemoveString
  function.
---

# arrayRemoveString

Removes value from array of strings.

## Signature

> arrayRemoveString('colName', value)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select RandomAirports, 
       arrayRemoveString(RandomAirports, 'SEA') AS value
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivAirportIDs</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SEA,PSC</td>
      <td>PSC</td>
    </tr>
    <tr>
      <td>SEA,PSC,PHX,MSY</td>
      <td>PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>SEA,PSC,PHX,MSY</td>
      <td>PSC,PHX,MSY</td>
    </tr>
    <tr>
      <td>SEA,PSC</td>
      <td>PSC</td>
    </tr>
    <tr>
      <td>SEA,PSC</td>
      <td>PSC</td>
    </tr>
  </tbody>
</table>
