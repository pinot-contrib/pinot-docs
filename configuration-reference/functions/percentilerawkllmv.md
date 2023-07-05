---
description: >-
  This section contains reference documentation for the PERCENTILERAWKLLMV function.
---

# PERCENTILRAWEKLLMV

Variant of the `PERCENTILERAWKLL` aggregation function which accepts multi-value columns. Values in the given column are 'flattened' before aggregation.

## Signature

> PercentileRAWKLLMV(column, percentile, kValue) -> Double

* `column` (required): Name of the column to aggregate on. 
* `percentile` (required): Percentile value to be calculated [0..100]
* `kValue`: Integer value which determines the size of the sketch. Default value is `200` which corresponds to a normalized rank error of about 1.65%. For defails please see the [accuracy vs size chart](https://datasketches.apache.org/docs/KLL/KLLAccuracyAndSize.html).

## Usage Examples

```sql
select percentileKLLMV(ArrOfInts, 90) as value
from MyTable
```

| sketch   |
| -------- |
| BQEPC... |
