---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTRAWCPCSKETCH function.
---

# DISTINCTCOUNTRAWCPCSKETCH

The [Compressed Probability Counting(CPC) Sketch](https://datasketches.apache.org/docs/CPC/CPC.html) enables extremely space-efficient cardinality estimation.  The stored CPC sketch can consume about 40% less space than an HLL sketch of comparable accuracy.  Pinot can aggregate multiple existing CPC sketches together to get a total distinct count or estimated directly from raw values.  This function call returns the sketch encoded as hexadecimal to the user.

## Signature

> distinctCountRawCpcSketch(**\<cpcSketchColumn>, \<cpcSketchParams>**) -> HexEncoded

* `cpcSketchColumn` (required): Name of the column to aggregate on.
* `cpcSketchParams` (required): Semicolon-separated parameter string for constructing the intermediate CPC sketches.
  * The supported parameters are:
   * `nominalEntries`: The nominal entries used to create the sketch. (Default 4096)
   * `accumulatorThreshold`: How many sketches should be kept in memory before merging. (Default 2)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select distinctCountRawCpcSketch(teamID) AS value
from baseballStats 
```

| value                                |
| ------------------------------------ |
| CAEQDAAOzJOVAAAAJwAAAAAAAAAMm69Al... |

```sql
select distinctCountRawCpcSketch(teamID, 'nominalEntries=256;accumulatorThreshold=10') AS value
from baseballStats 
```

| value                               |
| ----------------------------------- |
| CAEQCAAWzJOIAAAAEwAAAAAAAADAbGpA... |

We can also combine CPC sketches together via `cpcSketchUnion` for more complex use cases:

```sql
select
  cpcSketchUnion(
	  distinctCountRawCpcSketch(teamID) FILTER (WHERE yearID = 2004),
	  distinctCountRawCpcSketch(teamID) FILTER (WHERE league = 'NL')
  ) AS value
from baseballStats
```

| value                              |
| ---------------------------------- |
| 0401100c000acc933a000000120000e... |

This function can also be used with the V2 query engine.
