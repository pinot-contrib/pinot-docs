---
description: >-
  This section contains reference documentation for the arrayDistinctInt
  function.
---

# arrayDistinctInt

Returns unique values in an array of ints.

## Signature

> arrayDistinctInt('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayDistinctInt(DivAirportIDs) AS unique
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivAirportIDs</th>
      <th>unique</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>15016,11066</td>
      <td>15016,11066</td>
    </tr>
    <tr>
      <td>10620,14869</td>
      <td>10620,14869</td>
    </tr>
    <tr>
      <td>13891,12892</td>
      <td>13891,12892</td>
    </tr>
    <tr>
      <td>12264,10397</td>
      <td>12264,10397</td>
    </tr>
    <tr>
      <td>11066,12892</td>
      <td>11066,12892</td>
    </tr>
  </tbody>
</table>
