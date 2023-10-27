---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTRAWCPCSKETCH function.
---

# DISTINCTCOUNTRAWCPCSKETCH

The [Compressed Probability Counting(CPC) Sketch](https://datasketches.apache.org/docs/CPC/CPC.html) enables extremely space-efficient cardinality estimation.  The stored CPC sketch can consume about 40% less space than an HLL sketch of comparable accuracy.  Pinot can aggregate multiple existing CPC sketches together to get a total distinct count or estimated directly from raw values.  This function call returns the sketch encoded as hexadecimal to the user.

## Signature

> distinctCountRawCpcSketch(**\<cpcSketchColumn>, \<cpcSketchParam>**) -> HexEncoded

* `cpcSketchColumn` (required): Name of the column to aggregate on.
* `cpcSketchParam` (optional): lgK which is the the log2 of K, which controls both the size and accuracy of the sketch.  If not supplied, the Helix default is used.

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
select distinctCountRawCpcSketch(teamID, 8) AS value
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
