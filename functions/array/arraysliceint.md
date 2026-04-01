---
description: This section contains reference documentation for the arraySliceInt function.
---

# arraySliceInt

Returns the values in the array between the start and end positions.

## Signature

> arraySliceInt('colName', start, end)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arraySliceInt(DivAirportIDs, 0, 1) AS airports, 
	     DivAirportIDs
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>FlightNum</th>
      <th>airports</th>
      <th>DivAirportIDs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1531</td>
      <td>13891</td>
      <td>13891,12892</td>
    </tr>
    <tr>
      <td>19</td>
      <td>14683</td>
      <td>14683,14683</td>
    </tr>
    <tr>
      <td>829</td>
      <td>12339</td>
      <td>12339,12339</td>
    </tr>
    <tr>
      <td>24</td>
      <td>13198</td>
      <td>13198,10721</td>
    </tr>
    <tr>
      <td>548</td>
      <td>10721</td>
      <td>10721,12478</td>
    </tr>
  </tbody>
</table>
