---
description: Aggregate functions return a single result for a group of rows.
---

# Aggregation Functions

Aggregate functions return a single result for a group of rows. The pages below provide detailed signatures, usage examples, and notes for each function.

## Basic Aggregations

| Function | Description |
| -------- | ----------- |
| [COUNT](count.md) | Count of rows |
| [SUM](sum.md) / [SUMMV](summv.md) | Sum of values |
| [MIN](min.md) / [MINMV](minmv.md) | Minimum value |
| [MAX](max.md) / [MAXMV](maxmv.md) | Maximum value |
| [AVG](avg.md) / [AVGMV](avgmv.md) | Average of values |
| [MODE](mode.md) | Most frequent value |
| [HISTOGRAM](histogram.md) | Histogram of values |
| [SUMPRECISION](sumprecision.md) | High-precision sum using BigDecimal |
| [ANYVALUE](anyvalue.md) | Any arbitrary non-null value from a group |
| [BOOLAND](booland.md) / [BOOLOR](boolor.md) | Logical AND/OR across boolean values |

## Array and String Aggregations

| Function | Description |
| -------- | ----------- |
| [ARRAYAGG](arrayagg.md) | Collect values into an array |
| [LISTAGG](listagg.md) | Concatenate values into a delimited string |
| [SUMARRAYLONG](sumarraylong.md) | Element-wise sum of long arrays |
| [SUMARRAYDOUBLE](sumarraydouble.md) | Element-wise sum of double arrays |

## Statistical Functions

| Function | Description |
| -------- | ----------- |
| [SKEWNESS](skewness.md) | Skewness of a distribution |
| [KURTOSIS](kurtosis.md) | Kurtosis of a distribution |
| [DISTINCTSUM](distinctsum.md) / [DISTINCTAVG](distinctavg.md) | Sum/average of distinct values |
| [EXPRMIN](exprmin.md) / [EXPRMAX](exprmax.md) | Project columns at row with min/max measure |
| [ARG_MIN / ARG_MAX](arg_min-arg_max.md) | Project column at row with min/max measure |

## Set and Sketch Functions

| Function | Description |
| -------- | ----------- |
| [IDSET](idset.md) | Build an IdSet for efficient filtering |

For sketch-based functions (FrequentItems, CPC, HLL+, ULL, Tuple), see [Sketch Functions](../sketch/).
For funnel analysis functions, see [Funnel Functions](../funnel/).

## Distinct Counting

| Function | Description |
| -------- | ----------- |
| [DISTINCT](distinct.md) | Exact distinct values |
| [DISTINCTCOUNT](distinctcount.md) | Exact distinct count |
| [DISTINCTCOUNTBITMAP](distinctcountbitmap.md) | Distinct count using bitmap |
| [DISTINCTCOUNTHLL](distinctcounthll.md) | Approximate distinct count using HLL |
| [DISTINCTCOUNTTHETASKETCH](distinctcountthetasketch.md) | Distinct count using Theta sketch |
| [DISTINCTCOUNTSMARTHLL](distinctcountsmarthll.md) | Hybrid exact/HLL distinct count |

For sketch-based distinct count functions (CPC, HLL+, ULL, Tuple), see [Sketch Functions](../sketch/).

## Percentile Functions

| Function | Description |
| -------- | ----------- |
| [PERCENTILE](percentile.md) | Exact percentile |
| [PERCENTILEEST](percentileest.md) | Estimated percentile |
| [PERCENTILEKLL](percentilekll.md) | Percentile using KLL sketch |
| [PERCENTILETDIGEST](percentiletdigest.md) | Percentile using T-Digest |

## Window-Related Functions

| Function | Description |
| -------- | ----------- |
| [FIRST_VALUE](first_value.md) / [LAST_VALUE](last_value.md) | First/last value in window |
| [LEAD](lead.md) / [LAG](lag.md) | Access subsequent/preceding rows |
| [FIRSTWITHTIME](firstwithtime.md) / [LASTWITHTIME](lastwithtime.md) | First/last value by time |

## Multi-Value Column Functions

The following aggregation functions can be used for multi-value columns:

| Function | Description |
| -------- | ----------- |
| [COUNTMV](countmv.md) | Returns the count of a multi-value column |
| [MINMV](minmv.md) | Returns the minimum value of a numeric multi-value column |
| [MAXMV](maxmv.md) | Returns the maximum value of a numeric multi-value column |
| [SUMMV](summv.md) | Returns the sum of the values for a numeric multi-value column |
| [AVGMV](avgmv.md) | Returns the average of the values for a numeric multi-value column |
| [MINMAXRANGEMV](minmaxrangemv.md) | Returns the `max - min` value for a numeric multi-value column |
| [PERCENTILEMV](percentilemv.md) | Returns the Nth percentile of a numeric multi-value column |
| [PERCENTILEESTMV](percentileestmv.md) | Returns the Nth percentile using Quantile Digest for a multi-value column |
| [PERCENTILETDIGESTMV](percentiletdigestmv.md) | Returns the Nth percentile using T-Digest for a multi-value column |
| [DISTINCTCOUNTMV](distinctcountmv.md) | Returns the count of distinct values for a multi-value column |
| [DISTINCTCOUNTBITMAPMV](distinctcountbitmapmv.md) | Returns the count of distinct values using bitmap for a multi-value column |
| [DISTINCTCOUNTHLLMV](distinctcounthllmv.md) | Returns an approximate distinct count using HLL for a multi-value column |
| [DISTINCTCOUNTRAWHLLMV](distinctcountrawhllmv.md) | Returns HyperLogLog response serialized as string for a multi-value column |
| [DISTINCTSUMMV](distinctsummv.md) | Returns the sum of distinct values of a numeric multi-value column |
| [DISTINCTAVGMV](distinctavgmv.md) | Returns the average of distinct values of a numeric multi-value column |

For sketch-based multi-value functions (HLL+), see [Sketch Functions](../sketch/).

## FILTER Clause in Aggregation

Pinot supports the FILTER clause in aggregation queries:

```sql
SELECT SUM(COL1) FILTER (WHERE COL2 > 300),
       AVG(COL2) FILTER (WHERE COL2 < 50)
FROM MyTable WHERE COL3 > 50
```

In the query above, `COL1` is aggregated only for rows where `COL2 > 300 and COL3 > 50`. Similarly, `COL2` is aggregated where `COL2 < 50 and COL3 > 50`.

With [NULL Value Support](../../build-with-pinot/querying-and-sql/null-value-support.md) enabled, this allows filtering out null values while performing aggregation:

```sql
SELECT SUM(COL1) FILTER (WHERE COL1 IS NOT NULL)
FROM MyTable WHERE COL3 > 50
```

## Deprecated Functions

| Function | Description |
| -------- | ----------- |
| FASTHLL | Stores serialized HyperLogLog in String format. Performs worse than DISTINCTCOUNTHLL, which supports serialized HyperLogLog in BYTES format. |
| FASTHLLMV | Multi-value version of FASTHLL. Also deprecated in favor of DISTINCTCOUNTHLL. |

## Additional Reference Pages

| Function | Function |
| --- | --- |
| [DISTINCT_COUNT_OFF_HEAP](distinct_count_off_heap.md) | [DISTINCTCOUNTHLLPLUS](distinctcounthll-1.md) |
| [DISTINCTCOUNTRAWHLL](distinctcountrawhll.md) | [DISTINCTCOUNTRAWTHETASKETCH](distinctcountrawthetasketch.md) |
| [DISTINCTCOUNTULL](distinctcountull.md) | [FUNNELSTEPDURATIONSTATS](funnelstepdurationstats.md) |
| [maxString](maxstring.md) | [minmaxrange](minmaxrange.md) |
| [minString](minstring.md) | [percentilekllmv](percentilekllmv.md) |
| [percentilerawkll](percentilerawkll.md) | [percentilerawkllmv](percentilerawkllmv.md) |
| [SEGMENTPARTITIONEDDISTINCTCOUNT](segmentpartitioneddistinctcount.md) | [VALUEIN](valuein.md) |
