---
description: This section contains reference documentation for the ADD function.
---

# ADD

Sum of at least two values

## Signature

> ADD(col1, col2, col3...)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select homeRuns, baseOnBalls, ADD(homeRuns, baseOnBalls) AS total
from baseballStats 
WHERE teamID = 'ML1' 
AND yearID = 1956 
AND playerName = 'Henry Louis'
```

<table>
  <thead>
    <tr>
      <th>homeRuns</th>
      <th>baseOnBalls</th>
      <th>total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>26</td>
      <td>37</td>
      <td>63</td>
    </tr>
  </tbody>
</table>
