---
description: Aggregate functions return a single result for a group of rows.
---

# Aggregation Functions

Aggregate functions return a single result for a group of rows. The pages below provide detailed signatures, usage examples, and notes for each function.

## Basic Aggregations

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[COUNT](count.md)</td>
      <td>Count of rows</td>
    </tr>
    <tr>
      <td>[SUM](sum.md) / [SUMMV](summv.md)</td>
      <td>Sum of values</td>
    </tr>
    <tr>
      <td>[MIN](min.md) / [MINMV](minmv.md)</td>
      <td>Minimum value</td>
    </tr>
    <tr>
      <td>[MAX](max.md) / [MAXMV](maxmv.md)</td>
      <td>Maximum value</td>
    </tr>
    <tr>
      <td>[AVG](avg.md) / [AVGMV](avgmv.md)</td>
      <td>Average of values</td>
    </tr>
    <tr>
      <td>[MODE](mode.md)</td>
      <td>Most frequent value</td>
    </tr>
    <tr>
      <td>[HISTOGRAM](histogram.md)</td>
      <td>Histogram of values</td>
    </tr>
    <tr>
      <td>[SUMPRECISION](sumprecision.md)</td>
      <td>High-precision sum using BigDecimal</td>
    </tr>
    <tr>
      <td>[ANYVALUE](anyvalue.md)</td>
      <td>Any arbitrary non-null value from a group</td>
    </tr>
    <tr>
      <td>[BOOLAND](booland.md) / [BOOLOR](boolor.md)</td>
      <td>Logical AND/OR across boolean values</td>
    </tr>
  </tbody>
</table>

## Array and String Aggregations

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[ARRAYAGG](arrayagg.md)</td>
      <td>Collect values into an array</td>
    </tr>
    <tr>
      <td>[LISTAGG](listagg.md)</td>
      <td>Concatenate values into a delimited string</td>
    </tr>
    <tr>
      <td>[SUMARRAYLONG](sumarraylong.md)</td>
      <td>Element-wise sum of long arrays</td>
    </tr>
    <tr>
      <td>[SUMARRAYDOUBLE](sumarraydouble.md)</td>
      <td>Element-wise sum of double arrays</td>
    </tr>
  </tbody>
</table>

## Statistical Functions

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[SKEWNESS](skewness.md)</td>
      <td>Skewness of a distribution</td>
    </tr>
    <tr>
      <td>[KURTOSIS](kurtosis.md)</td>
      <td>Kurtosis of a distribution</td>
    </tr>
    <tr>
      <td>[DISTINCTSUM](distinctsum.md) / [DISTINCTAVG](distinctavg.md)</td>
      <td>Sum/average of distinct values</td>
    </tr>
    <tr>
      <td>[EXPRMIN](exprmin.md) / [EXPRMAX](exprmax.md)</td>
      <td>Project columns at row with min/max measure</td>
    </tr>
    <tr>
      <td>[ARG_MIN / ARG_MAX](arg_min-arg_max.md)</td>
      <td>Project column at row with min/max measure</td>
    </tr>
  </tbody>
</table>

## Set and Sketch Functions

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[IDSET](idset.md)</td>
      <td>Build an IdSet for efficient filtering</td>
    </tr>
  </tbody>
</table>

For sketch-based functions (FrequentItems, CPC, HLL+, ULL, Tuple), see [Sketch Functions](../sketch/).
For funnel analysis functions, see [Funnel Functions](../funnel/).

## Distinct Counting

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[DISTINCT](distinct.md)</td>
      <td>Exact distinct values</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNT](distinctcount.md)</td>
      <td>Exact distinct count</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTBITMAP](distinctcountbitmap.md)</td>
      <td>Distinct count using bitmap</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTHLL](distinctcounthll.md)</td>
      <td>Approximate distinct count using HLL</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTTHETASKETCH](distinctcountthetasketch.md)</td>
      <td>Distinct count using Theta sketch</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTSMARTHLL](distinctcountsmarthll.md)</td>
      <td>Hybrid exact/HLL distinct count</td>
    </tr>
  </tbody>
</table>

For sketch-based distinct count functions (CPC, HLL+, ULL, Tuple), see [Sketch Functions](../sketch/).

## Percentile Functions

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[PERCENTILE](percentile.md)</td>
      <td>Exact percentile</td>
    </tr>
    <tr>
      <td>[PERCENTILEEST](percentileest.md)</td>
      <td>Estimated percentile</td>
    </tr>
    <tr>
      <td>[PERCENTILEKLL](percentilekll.md)</td>
      <td>Percentile using KLL sketch</td>
    </tr>
    <tr>
      <td>[PERCENTILETDIGEST](percentiletdigest.md)</td>
      <td>Percentile using T-Digest</td>
    </tr>
  </tbody>
</table>

## Window-Related Functions

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[FIRST_VALUE](first_value.md) / [LAST_VALUE](last_value.md)</td>
      <td>First/last value in window</td>
    </tr>
    <tr>
      <td>[LEAD](lead.md) / [LAG](lag.md)</td>
      <td>Access subsequent/preceding rows</td>
    </tr>
    <tr>
      <td>[FIRSTWITHTIME](firstwithtime.md) / [LASTWITHTIME](lastwithtime.md)</td>
      <td>First/last value by time</td>
    </tr>
  </tbody>
</table>

## Multi-Value Column Functions

The following aggregation functions can be used for multi-value columns:

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[COUNTMV](countmv.md)</td>
      <td>Returns the count of a multi-value column</td>
    </tr>
    <tr>
      <td>[MINMV](minmv.md)</td>
      <td>Returns the minimum value of a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[MAXMV](maxmv.md)</td>
      <td>Returns the maximum value of a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[SUMMV](summv.md)</td>
      <td>Returns the sum of the values for a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[AVGMV](avgmv.md)</td>
      <td>Returns the average of the values for a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[MINMAXRANGEMV](minmaxrangemv.md)</td>
      <td>Returns the `max - min` value for a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[PERCENTILEMV](percentilemv.md)</td>
      <td>Returns the Nth percentile of a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[PERCENTILEESTMV](percentileestmv.md)</td>
      <td>Returns the Nth percentile using Quantile Digest for a multi-value column</td>
    </tr>
    <tr>
      <td>[PERCENTILETDIGESTMV](percentiletdigestmv.md)</td>
      <td>Returns the Nth percentile using T-Digest for a multi-value column</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTMV](distinctcountmv.md)</td>
      <td>Returns the count of distinct values for a multi-value column</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTBITMAPMV](distinctcountbitmapmv.md)</td>
      <td>Returns the count of distinct values using bitmap for a multi-value column</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTHLLMV](distinctcounthllmv.md)</td>
      <td>Returns an approximate distinct count using HLL for a multi-value column</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWHLLMV](distinctcountrawhllmv.md)</td>
      <td>Returns HyperLogLog response serialized as string for a multi-value column</td>
    </tr>
    <tr>
      <td>[DISTINCTSUMMV](distinctsummv.md)</td>
      <td>Returns the sum of distinct values of a numeric multi-value column</td>
    </tr>
    <tr>
      <td>[DISTINCTAVGMV](distinctavgmv.md)</td>
      <td>Returns the average of distinct values of a numeric multi-value column</td>
    </tr>
  </tbody>
</table>

For sketch-based multi-value functions (HLL+), see [Sketch Functions](../sketch/).

## FILTER Clause in Aggregation

Pinot supports the FILTER clause in aggregation queries:

```sql
SELECT SUM(COL1) FILTER (WHERE COL2 > 300),
       AVG(COL2) FILTER (WHERE COL2 < 50)
FROM MyTable WHERE COL3 > 50
```

In the query above, `COL1` is aggregated only for rows where `COL2 > 300 and COL3 > 50`. Similarly, `COL2` is aggregated where `COL2 < 50 and COL3 > 50`.

With [NULL Value Support](../../developers/advanced/null-value-support.md) enabled, this allows filtering out null values while performing aggregation:

```sql
SELECT SUM(COL1) FILTER (WHERE COL1 IS NOT NULL)
FROM MyTable WHERE COL3 > 50
```

## Deprecated Functions

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>FASTHLL</td>
      <td>Stores serialized HyperLogLog in String format. Performs worse than DISTINCTCOUNTHLL, which supports serialized HyperLogLog in BYTES format.</td>
    </tr>
    <tr>
      <td>FASTHLLMV</td>
      <td>Multi-value version of FASTHLL. Also deprecated in favor of DISTINCTCOUNTHLL.</td>
    </tr>
  </tbody>
</table>

## Additional Reference Pages

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Function</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[DISTINCT_COUNT_OFF_HEAP](distinct_count_off_heap.md)</td>
      <td>[DISTINCTCOUNTHLLPLUS](distinctcounthll-1.md)</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTRAWHLL](distinctcountrawhll.md)</td>
      <td>[DISTINCTCOUNTRAWTHETASKETCH](distinctcountrawthetasketch.md)</td>
    </tr>
    <tr>
      <td>[DISTINCTCOUNTULL](distinctcountull.md)</td>
      <td>[FUNNELSTEPDURATIONSTATS](funnelstepdurationstats.md)</td>
    </tr>
    <tr>
      <td>[maxString](maxstring.md)</td>
      <td>[minmaxrange](minmaxrange.md)</td>
    </tr>
    <tr>
      <td>[minString](minstring.md)</td>
      <td>[percentilekllmv](percentilekllmv.md)</td>
    </tr>
    <tr>
      <td>[percentilerawkll](percentilerawkll.md)</td>
      <td>[percentilerawkllmv](percentilerawkllmv.md)</td>
    </tr>
    <tr>
      <td>[SEGMENTPARTITIONEDDISTINCTCOUNT](segmentpartitioneddistinctcount.md)</td>
      <td>[VALUEIN](valuein.md)</td>
    </tr>
  </tbody>
</table>
