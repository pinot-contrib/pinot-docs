---
description: >-
  Reference documentation for aggregation functions in Apache Pinot.
---

# Aggregation Functions

For the full aggregation function reference table, see [Supported Aggregations](../../users/user-guide-query/supported-aggregations.md).

This directory contains individual reference pages for each aggregation function. The pages below provide detailed signatures, usage examples, and notes.

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
