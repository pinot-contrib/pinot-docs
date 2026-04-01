---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLLPLUS
  function.
---

# DISTINCTCOUNTHLLPLUS

Returns an approximate distinct count using _HyperLogLogPlusPlus_. It also takes an optional second and third arguments to configure the _p_, _sp_ for the _HyperLogLogPlus_.\
The optional parameter _p_ defines the normal set precision and the parameter _sp_ defines the sparse set precision.\
For accurate distinct counting, see [DISTINCTCOUNT](../aggregation/distinctcount.md).

## Signature

> DISTINCTCOUNTHLLPlus(colName)
> DISTINCTCOUNTHLLPlus(colName, p)
> DISTINCTCOUNTHLLPlus(colName, p, sp)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCTCOUNTHLLPLUS(teamID) AS value
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
      <td>158</td>
    </tr>
  </tbody>
</table>

```sql
select DISTINCTCOUNTHLLPLUS(teamID, 12) AS value
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
      <td>149</td>
    </tr>
  </tbody>
</table>
