---
description: >-
  This section contains reference documentation for the arrayContainsInt
  function.
---

# arrayContainsInt

Checks if int value exists in array.

## Signature

> arrayContainsInt('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayContainsInt(DivAirportIDs, 14683) AS containsValue
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivAirportIDs</th>
      <th>containsValue</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13891,12892</td>
      <td>false</td>
    </tr>
    <tr>
      <td>14683,14683</td>
      <td>true</td>
    </tr>
    <tr>
      <td>12339,12339</td>
      <td>false</td>
    </tr>
    <tr>
      <td>13487,13930</td>
      <td>false</td>
    </tr>
    <tr>
      <td>13029,11292</td>
      <td>false</td>
    </tr>
  </tbody>
</table>
