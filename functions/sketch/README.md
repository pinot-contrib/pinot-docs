---
description: >-
  Reference documentation for approximate distinct count and sketch-based
  aggregation functions in Apache Pinot.
---

# Sketch Functions

Pinot supports several sketch-based algorithms for approximate distinct counting and summarization. These functions trade a small amount of accuracy for significant memory and performance savings at scale.

For exact distinct counting, see [DISTINCTCOUNT](../aggregation/distinctcount.md).

## CPC Sketch

The [Compressed Probability Counting (CPC) Sketch](https://datasketches.apache.org/docs/CPC/CPC.html) enables extremely space-efficient cardinality estimation — about 40% less space than an HLL sketch of comparable accuracy.

| Function | Description |
| -------- | ----------- |
| [DISTINCTCOUNTCPCSKETCH](distinctcountcpcsketch.md) | Returns approximate distinct count using CPC sketch |
| [DISTINCTCOUNTRAWCPCSKETCH](distinctcountrawcpcsketch.md) | Returns raw CPC sketch as hex string |

## HyperLogLog Plus

HyperLogLogPlus (HLL++) provides approximate distinct counts with configurable precision (`p`, `sp` parameters).

| Function | Description |
| -------- | ----------- |
| [DISTINCTCOUNTHLLPLUS](distinctcounthllplus.md) | Approximate distinct count using HLL++ |
| [DISTINCTCOUNTSMARTHLLPLUS](distinctcounthllplus.md#distinctcountsmarthllplus) | Starts exact and converts to HLL++ after a threshold |
| [DISTINCTCOUNTHLLPLUSMV](distinctcounthllplusmv.md) | HLL++ for multi-value columns |
| [DISTINCTCOUNTRAWHLLPLUS](distinctcountrawhllplus.md) | Returns serialized HLL++ sketch |
| [DISTINCTCOUNTRAWHLLPLUSMV](distinctcountrawhllplusmv.md) | Serialized HLL++ sketch for multi-value columns |

## UltraLogLog

The [UltraLogLog Sketch](https://arxiv.org/abs/2308.16862) from Dynatrace requires less space than HyperLogLog and provides a simpler, faster estimator. Implemented via [Hash4j](https://github.com/dynatrace-oss/hash4j/tree/main).

| Function | Description |
| -------- | ----------- |
| [DISTINCTCOUNTULL](distinctcountull.md) | Approximate distinct count using ULL (default p=12) |
| [DISTINCTCOUNTRAWULL](distinctcountrawull.md) | Returns serialized ULL sketch |

## Tuple Sketch

The [Tuple Sketch](https://datasketches.apache.org/docs/Tuple/TupleOverview.html) extends the Theta Sketch with additional summary values per entry, ideal for summarizing attributes like impressions or clicks.

| Function | Description |
| -------- | ----------- |
| [DISTINCTCOUNTTUPLESKETCH](distinctcounttuplesketch.md) | Distinct count from tuple sketch |
| [DISTINCTCOUNTRAWINTEGERSUMTUPLESKETCH](distinctcountrawintegersumtuplesketch.md) | Raw tuple sketch as hex |
| [AVGVALUEINTEGERSUMTUPLESKETCH](avgvalueintegersumtuplesketch.md) | Average of summary values |
| [SUMVALUESINTEGERSUMTUPLESKETCH](sumvaluesintegersumtuplesketch.md) | Sum of summary values |

With advanced null handling enabled, integer tuple-sketch aggregations skip rows whose sketch column is null. If no sketches contribute, `DISTINCTCOUNTTUPLESKETCH` and `SUMVALUESINTEGERSUMTUPLESKETCH` return `NULL`, `DISTINCTCOUNTRAWINTEGERSUMTUPLESKETCH` returns `NULL`, and `AVGVALUEINTEGERSUMTUPLESKETCH` returns `NULL`. Without advanced null handling, Pinot aggregates the column's default null value and preserves the legacy empty-sketch identities.

## Frequency Sketches

| Function | Description |
| -------- | ----------- |
| [FREQUENTLONGSSKETCH](frequentlongssketch.md) | Frequent items sketch for long values |
| [FREQUENTSTRINGSSKETCH](frequentstringssketch.md) | Frequent items sketch for string values |

With advanced null handling enabled, frequency-sketch functions skip null rows and return `NULL` when no values contribute. Without advanced null handling, the column's default null value contributes to the frequency estimate.
