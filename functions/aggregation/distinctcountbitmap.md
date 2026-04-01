---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTBITMAP
  function.
---

# DISTINCTCOUNTBITMAP

Returns the count of distinct row values in a group. This function is accurate for _INT_ column, but approximate for other cases where hash codes are used in distinct counting and there may be hash collisions.\
For accurate distinct counting on all column types, see [DISTINCTCOUNT](distinctcount.md).

## Signature

> DISTINCTCOUNTBITMAP(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCTCOUNTBITMAP(league) AS value
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
      <td>7</td>
    </tr>
  </tbody>
</table>

```sql
select DISTINCTCOUNTBITMAP(teamID) AS value
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
      <td>148</td>
    </tr>
  </tbody>
</table>
