---
description: This section contains reference documentation for the arraySortInt function.
---

# arraySortInt

Sorts array of ints.

## Signature

> arraySortInt('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arraySortInt(DivAirportIDs) AS sortedIds
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivAirportIDs</th>
      <th>sortedIds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13891,12892</td>
      <td>12892,13891</td>
    </tr>
    <tr>
      <td>14683,14683</td>
      <td>14683,14683</td>
    </tr>
    <tr>
      <td>12339,12339</td>
      <td>12339,12339</td>
    </tr>
    <tr>
      <td>13198,10721</td>
      <td>10721,13198</td>
    </tr>
    <tr>
      <td>10721,12478</td>
      <td>10721,12478</td>
    </tr>
  </tbody>
</table>
