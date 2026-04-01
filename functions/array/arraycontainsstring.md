---
description: >-
  This section contains reference documentation for the arrayContainsString
  function.
---

# arrayContainsString

Checks if string value exists in array.

## Signature

> arrayContainsString('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivTailNums, 
       arrayContainsString(DivTailNums, 'N7713A') AS index
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

<table>
  <thead>
    <tr>
      <th>DivTailNums</th>
      <th>index</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>N7713A,N7713A</td>
      <td>true</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
      <td>false</td>
    </tr>
    <tr>
      <td>N7713A,N7713A</td>
      <td>true</td>
    </tr>
  </tbody>
</table>
