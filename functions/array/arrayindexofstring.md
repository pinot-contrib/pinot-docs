---
description: >-
  This section contains reference documentation for the arrayIndexOfString
  function.
---

# arrayIndexOfString

Finds the last index of the given value in the array starting at the given index.

## Signature

> arrayIndexOfString('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivTailNums, 
       arrayIndexOfString(DivTailNums, 'N7713A') AS index
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
      <td>0</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
      <td>-1</td>
    </tr>
    <tr>
      <td>N7713A,N7713A</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
