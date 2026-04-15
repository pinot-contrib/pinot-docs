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

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select DISTINCTCOUNTHLLPLUS(teamID) AS value
from baseballStats 
```

| value |
| ----- |
| 158   |

```sql
select DISTINCTCOUNTHLLPLUS(teamID, 12) AS value
from baseballStats 
```

| value |
| ----- |
| 149   |

## DISTINCTCOUNTSMARTHLLPLUS

`DISTINCTCOUNTSMARTHLLPLUS` starts with exact distinct counting in a set and switches to HyperLogLog++ when the number of distinct values exceeds a threshold. This is useful when some groups stay small enough for exact counting while larger groups still need bounded memory usage.

### Signature

> DISTINCTCOUNTSMARTHLLPLUS(colName)
> DISTINCTCOUNTSMARTHLLPLUS(colName, 'threshold=<n>;p=<p>;sp=<sp>')

### Parameters

* `colName` (required): Column to aggregate.
* `threshold` (optional): Number of distinct values Pinot keeps exactly before converting to HLL++. Default: `100000`. A non-positive value disables the conversion.
* `p` (optional): HyperLogLog++ normal precision after conversion. Default: `14`.
* `sp` (optional): HyperLogLog++ sparse precision after conversion. Default: `0`.

### Usage Examples

```sql
SELECT DISTINCTCOUNTSMARTHLLPLUS(teamID) AS value
FROM baseballStats
```

```sql
SELECT DISTINCTCOUNTSMARTHLLPLUS(teamID, 'threshold=10000;p=12') AS value
FROM baseballStats
```
