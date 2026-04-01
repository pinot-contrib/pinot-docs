---
description: This section contains reference documentation for the EXPRMAX function.
---

# EXPRMAX

Projects one or more columns from the row where a measuring column has its maximum value. Similar to ARG\_MAX but supports projecting multiple expression columns at once.

## Signature

> EXPRMAX(measureCol, exprCol1, exprCol2, ...)

Parameters:

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`measureCol`</td>
      <td>The column whose maximum value determines which row to project from</td>
    </tr>
    <tr>
      <td>`exprCol1, exprCol2, ...`</td>
      <td>One or more columns to project from the row with the maximum measure</td>
    </tr>
  </tbody>
</table>

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select EXPRMAX(hits, playerName, yearID) AS value
from baseballStats
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Ichiro Suzuki, 2004]</td>
    </tr>
  </tbody>
</table>
