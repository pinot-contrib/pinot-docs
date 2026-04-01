---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTMV
  function.
---

# DISTINCTCOUNTMV

Returns the count of distinct row values in a group

## Signature

> DISTINCTCOUNTMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

The following query returns the documents that have a `DivTailNums` with more than one value:

```sql
select DivTailNums
from airlineStats 
where arraylength(DivTailNums) > 1
```

<table>
  <thead>
    <tr>
      <th>DivTailNums</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>N7713A,N7713A</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
    </tr>
    <tr>
      <td>N344AA,N344AA</td>
    </tr>
    <tr>
      <td>N7713A,N7713A</td>
    </tr>
  </tbody>
</table>

You can count the distinct number of items in these rows by running the following query:

```sql
select DISTINCTCOUNTMV(DivTailNums) AS value
from airlineStats 
where arraylength(DivTailNums) > 1
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2</td>
    </tr>
  </tbody>
</table>
