---
description: >-
  This section contains reference documentation for the arrayReverseInt
  function.
---

# arrayReverseInt

Reverses array of ints.

## Signature

> arrayReverseInt('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayReverseInt(DivAirportIDs) AS reversedIds
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivAirportIDs</th>
      <th>reversedIds</th>
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
      <td>13487,13930</td>
      <td>13930,13487</td>
    </tr>
    <tr>
      <td>13029,11292</td>
      <td>11292,13029</td>
    </tr>
  </tbody>
</table>
