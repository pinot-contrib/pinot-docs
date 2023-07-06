---
description: >-
  This section contains reference documentation for the PERCENTILEKLL function.
---

# PERCENTILEKLL

`KLL Sketch` is an approxiamate quantiles algorithm which targets optimal space for a given accuracy. `PERCENTILEKLL` is a percentile calculation aggregation function based on Apache Datasketches [KLL Doubles Sketch](https://datasketches.apache.org/docs/KLL/KLLSketch.html) implementation.

Pinot also offers a 'raw' variant, `PERCENTILEKLLRAW`, which returns the serialized sketch that can be used for calculating 'rank' or 'histogram'.

All of the variants of `PercentileKLL` also support raw sketches in Pinot columns. This means you can create KLL Doubles sketches outside of Pinot and ingest them into columns as binary strings. `PercentileKLL` will identify these columns merge them to produce aggregate results.

## Signature

> PercentileKLL(column, percentile, kValue) -> Double

* `column` (required): Name of the column to aggregate on. If the column is a multi value column, use `PERCENTILEKLLMV` variant.
* `percentile` (required): Percentile value to be calculated [0..100]
* `kValue`: Integer value which determines the size of the sketch. Default value is `200` which corresponds to a normalized rank error of about 1.65%. For details please see the [accuracy vs size chart](https://datasketches.apache.org/docs/KLL/KLLAccuracyAndSize.html).

## Usage Examples

```sql
select percentileKLL(ArrDelayMinutes, 90) as DelayP90
from airlineStats
```

| DelayP90 |
| -------- |
| 40       |

```sql
select Carrier, percentileKll(ArrDelay, 50, 600) as MedianDelay
from airlineStats
where ArrDelay > 0
group by Carrier
order by 2 desc
limit 3
```

| Carrier |	MedianDelay |
| ------- | ----------- |
| MQ      | 28          |
| B6      | 28          |
| EV      | 24          |

