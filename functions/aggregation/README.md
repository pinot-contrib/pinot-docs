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
| [AVG](avgmv.md) | Average of values |
| [MODE](mode.md) | Most frequent value |
| [HISTOGRAM](histogram.md) | Histogram of values |

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
