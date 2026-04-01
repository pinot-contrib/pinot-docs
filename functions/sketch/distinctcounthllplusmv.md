---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLLPLUSMV
  function.
---

# DISTINCTCOUNTHLLPLUSMV

Returns an approximate distinct count using HyperLogLogPlusPlus in a group.\
The optional parameter _p_ defines the normal set precision and the parameter _sp_ defines the sparse set precision.

## Signature

> DISTINCTCOUNTHLLPLUSMV(colName)
> DISTINCTCOUNTHLLPLUSMV(colName, p)
> DISTINCTCOUNTHLLPLUSMV(colName, p, sp)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DISTINCTCOUNTHLLPLUSMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>34</td>
    </tr>
  </tbody>
</table>
