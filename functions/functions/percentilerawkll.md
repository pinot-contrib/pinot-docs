---
description: >-
  This section contains reference documentation for the PERCENTILERAWKLL function.
---

# PERCENTILERAWKLL

Raw variant of the `PERCENTILEKLL` which returns a Base64 encoded string of the KLLSketch object. The response can be deserialized back to a KLLSketch using Apache Datasketches library and used to do further analysis. For example you can use this approach to calculate the CDF (Cumulative Density Function) or PMF (Probability Mass Function) of a dataset.

## Signature

> PercentileRawKLL(column, percentile, kValue) -> Double

* `column` (required): Name of the column to aggregate on. If the column is a multi value column, use `PERCENTILERAWKLLMV` variant.
* `percentile` (required): Percentile value to be calculated [0..100]. For 'raw' versions of the function, this value is used for ordering (ORDER BY).

## Usage Examples

```sql
select percentileRawKll(ArrDelayMinutes, 90) as sketch
from airlineStats
```

| sketch   |
| -------- |
| BQEPC... |
