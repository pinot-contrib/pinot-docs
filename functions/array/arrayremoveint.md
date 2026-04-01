---
description: This section contains reference documentation for the arrayRemoveInt function.
---

# arrayRemoveInt

Removes value from array of ints.

## Signature

> arrayRemoveInt('colName', value)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayRemoveInt(DivAirportIDs, 12892) AS value
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
AND arrayContainsInt(DivAirportIDs, 12892) = 1
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
      <td>13891,12892</td>
      <td>13891</td>
    </tr>
    <tr>
      <td>13198,12892</td>
      <td>13198</td>
    </tr>
    <tr>
      <td>11066,12892</td>
      <td>11066</td>
    </tr>
    <tr>
      <td>13198,12892</td>
      <td>13198</td>
    </tr>
    <tr>
      <td>13891,12892</td>
      <td>13891</td>
    </tr>
  </tbody>
</table>
