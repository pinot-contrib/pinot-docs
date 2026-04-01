---
description: >-
  This section contains reference documentation for the arrayIndexOfInt
  function.
---

# arrayIndexOfInt

Finds the last index of the given value in the array starting at the given index.

## Signature

> arrayIndexOfInt('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayIndexOfInt(DivAirportIDs, 14683) AS index
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivAirportIDs</th>
      <th>index</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13891,12892</td>
      <td>-1</td>
    </tr>
    <tr>
      <td>14683,14683</td>
      <td>0</td>
    </tr>
    <tr>
      <td>12339,12339</td>
      <td>-1</td>
    </tr>
    <tr>
      <td>13487,13930</td>
      <td>-1</td>
    </tr>
    <tr>
      <td>13029,11292</td>
      <td>-1</td>
    </tr>
  </tbody>
</table>
