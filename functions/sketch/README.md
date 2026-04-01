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

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[DISTINCTCOUNTCPCSKETCH](distinctcountcpcsketch.md)</td>
      <td>Returns approximate distinct count using CPC sketch</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWCPCSKETCH](distinctcountrawcpcsketch.md)</td>
      <td>Returns raw CPC sketch as hex string</td>
    </tr>
  </tbody>
</table>

## HyperLogLog Plus

HyperLogLogPlus (HLL++) provides approximate distinct counts with configurable precision (`p`, `sp` parameters).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[DISTINCTCOUNTHLLPLUS](distinctcounthllplus.md)</td>
      <td>Approximate distinct count using HLL++</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTHLLPLUSMV](distinctcounthllplusmv.md)</td>
      <td>HLL++ for multi-value columns</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWHLLPLUS](distinctcountrawhllplus.md)</td>
      <td>Returns serialized HLL++ sketch</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWHLLPLUSMV](distinctcountrawhllplusmv.md)</td>
      <td>Serialized HLL++ sketch for multi-value columns</td>
    </tr>
  </tbody>
</table>

## UltraLogLog

The [UltraLogLog Sketch](https://arxiv.org/abs/2308.16862) from Dynatrace requires less space than HyperLogLog and provides a simpler, faster estimator. Implemented via [Hash4j](https://github.com/dynatrace-oss/hash4j/tree/main).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[DISTINCTCOUNTULL](distinctcountull.md)</td>
      <td>Approximate distinct count using ULL (default p=12)</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWULL](distinctcountrawull.md)</td>
      <td>Returns serialized ULL sketch</td>
    </tr>
  </tbody>
</table>

## Tuple Sketch

The [Tuple Sketch](https://datasketches.apache.org/docs/Tuple/TupleOverview.html) extends the Theta Sketch with additional summary values per entry, ideal for summarizing attributes like impressions or clicks.

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[DISTINCTCOUNTTUPLESKETCH](distinctcounttuplesketch.md)</td>
      <td>Distinct count from tuple sketch</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWINTEGERSUMTUPLESKETCH](distinctcountrawintegersumtuplesketch.md)</td>
      <td>Raw tuple sketch as hex</td>
    </tr>
    <tr>
      <td>[AVGVALUEINTEGERSUMTUPLESKETCH](avgvalueintegersumtuplesketch.md)</td>
      <td>Average of summary values</td>
    </tr>
    <tr>
      <td>[SUMVALUESINTEGERSUMTUPLESKETCH](sumvaluesintegersumtuplesketch.md)</td>
      <td>Sum of summary values</td>
    </tr>
  </tbody>
</table>

## Frequency Sketches

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[FREQUENTLONGSSKETCH](frequentlongssketch.md)</td>
      <td>Frequent items sketch for long values</td>
    </tr>
    <tr>
      <td>[FREQUENTSTRINGSSKETCH](frequentstringssketch.md)</td>
      <td>Frequent items sketch for string values</td>
    </tr>
  </tbody>
</table>
