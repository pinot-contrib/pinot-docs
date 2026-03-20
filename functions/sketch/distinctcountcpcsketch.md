---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTCPCSKETCH function.
---

# DISTINCTCOUNTCPCSKETCH

The [Compressed Probability Counting(CPC) Sketch](https://datasketches.apache.org/docs/CPC/CPC.html) enables extremely space-efficient cardinality estimation.  The stored CPC sketch can consume about 40% less space than an HLL sketch of comparable accuracy.  Pinot can aggregate multiple existing CPC sketches together to get a total distinct count or estimated directly from raw values.

For exact distinct counting, see [DISTINCTCOUNT](distinctcount.md).

## Signature

> distinctCountCpcSketch(**\<cpcSketchColumn>, \<cpcSketchParams>**) -> Long

* `cpcSketchColumn` (required): Name of the column to aggregate on.
* `cpcSketchParams` (required): Semicolon-separated parameter string for constructing the intermediate CPC sketches.
  * The supported parameters are:
   * `nominalEntries`: The nominal entries used to create the sketch. (Default 4096)
   * `accumulatorThreshold`: How many sketches should be kept in memory before merging. (Default 2)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select distinctCountCpcSketch(teamID) AS value
from baseballStats 
```

| value |
| ----- |
| 150   |

```sql
select distinctCountCpcSketch(teamID, 'nominalEntries=256;accumulatorThreshold=10') AS value
from baseballStats 
```

| value |
| ----- |
| 150   |

We can also extract estimates when combining CPC sketches together via `cpcSketchUnion`  for more complex use cases:

```sql
select
  getCpcSketchEstimate(
    cpcSketchUnion(
	    distinctCountRawCpcSketch(teamID) FILTER (WHERE yearID = 2004),
	    distinctCountRawCpcSketch(teamID) FILTER (WHERE league = 'NL')
    )
  ) AS value
from baseballStats
```

| value |
| ----- |
| 58    |

This function can also be used with the V2 query engine.
