---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTTUPLESKETCH
  function.
---

# DISTINCTCOUNTTUPLESKETCH

The [Tuple Sketch](https://datasketches.apache.org/docs/Tuple/TupleOverview.html) is an extension of the [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html).  Tuple sketches store an additional summary value with each retained entry which makes the sketch ideal for summarizing attributes such as impressions or clicks.  Tuple sketches are interoperable with the Theta Sketch and enable set operations over a stream of data, and can also be used for cardinality estimation.

## Signature

> distinctCountTupleSketch(**\<tupleSketchColumn>, \<tupleSketchParam>**) -> Long

* `tupleSketchColumn` (required): Name of the column to aggregate on.  This must be an existing tuple sketch serialized as bytes.
* `tupleSketchParam` (optional): lgK which is the the log2 of K, which controls both the size and accuracy of the sketch.  If not supplied, the Helix default is used.

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).  A new Tuple Sketch metric called `playerHomeRuns` was created during ingestion by updating the ingestion config as follows:

```json
	"ingestionConfig": {
		"transformConfigs": [
			{
				"columnName": "playerHomeRuns",
				"transformFunction": "toIntegerSumTupleSketch(playerID, homeRuns)"
			}
		]
	}
```

The `distinctCountTupleSketch` function can be used to extract an estimate of the number of unique items in a Tuple sketch.

```sql
select distinctCountTupleSketch(playerHomeRuns) as value
from baseballStats 
```

| value |
| ----- |
| 17549 |

```sql
select distinctCountTupleSketch(playerHomeRuns, 16) as value
from baseballStats 
```

| value |
| ----- |
| 17549 |

This function can also be used with the V2 query engine.
