---
description: This section contains reference documentation for the DISTINCTCOUNTRAWHLLMV function.
---

# DISTINCTCOUNTRAWHLLMV

Returns HLL response serialized as string. 
The serialized HLL can be converted back into an HLL and then aggregated with other HLLs. A common use case may be to merge HLL responses from different Pinot tables, or to allow aggregation after client-side batching.

## Signature

> DISTINCTCOUNTRAWHLLMV(colName, log2m)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DISTINCTCOUNTRAWHLLMV(DivAirports) AS value
from airlineStats 
where arraylength(DivAirports) > 1
```

| value   | 
| ------------- |
| 00000008000000ac00000000000000000000000500000020000000000030000202108000040000010000000300010400000000000000000000000463000000000000000000010001041000200000002000000000000000000a00000000028001000000010800000000010000001008000000804000000000020000040000880000000000000000000000000000000000000000000000800000000800020004000000840000000002000000000000000000001400 | 


```sql
select DISTINCTCOUNTRAWHLLMV(DivAirports, 1) AS value
from airlineStats 
where arraylength(DivAirports) > 1
```

| value   | 
| ------------- |
| 0000000100000004000000e4 | 