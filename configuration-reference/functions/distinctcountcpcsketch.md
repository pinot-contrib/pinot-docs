---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTCPCSKETCH function.
---

# DISTINCTCOUNTCPCSKETCH

The [Compressed Probability Counting(CPC) Sketch](https://datasketches.apache.org/docs/CPC/CPC.html) enables extremely space-efficient cardinality estimation.  The stored CPC sketch can consume about 40% less space than an HLL sketch of comparable accuracy.  Pinot can aggregate multiple existing CPC sketches together to get a total distinct count or estimated directly from raw values.

For exact distinct counting, see [DISTINCTCOUNT](distinctcount.md).

## Signature

> distinctCountCpcSketch(**\<cpcSketchColumn>, \<cpcSketchLgK>**) -> Long

* `cpcSketchColumn` (required): Name of the column to aggregate on.
* `cpcSketchLgK` (optional): lgK which is the the log2 of K, which controls both the size and accuracy of the sketch.  If not supplied, the Helix default is used.

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
select distinctCountCpcSketch(teamID, 8) AS value
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
