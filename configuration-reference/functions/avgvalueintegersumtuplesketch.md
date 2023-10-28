---
description: >-
  This section contains reference documentation for the AVGVALUEINTEGERSUMTUPLESKETCH
  function.
---

# AVGVALUEINTEGERSUMTUPLESKETCH

The [Tuple Sketch](https://datasketches.apache.org/docs/Tuple/TupleOverview.html) is an extension of the [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html).  Tuple sketches store an additional summary value with each retained entry which makes the sketch ideal for summarizing attributes such as impressions or clicks.  Tuple sketches are interoperable with the Theta Sketch and enable set operations over a stream of data, and can also be used for cardinality estimation.

## Signature

> avgValueIntegerSumTupleSketch(**\<tupleSketchColumn>, \<tupleSketchLgK>**) -> Long

* `tupleSketchColumn` (required): Name of the column to aggregate on.  This must be an existing tuple sketch serialized as bytes.
* `tupleSketchLgK` (optional): lgK which is the the log2 of K, which controls both the size and accuracy of the sketch.  If not supplied, the Helix default is used.

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

The `avgValueIntegerSumTupleSketch` function can be used to combine the summary values from the random sample stored within the Tuple sketch and formulate an estimate for an average that applies to the entire dataset.  The average should be interpreted as applying to each key tracked by the sketch - for example, average home runs per player.

```sql
select avgValueIntegerSumTupleSketch(playerHomeRuns) as value
from baseballStats 
```

| value |
| ----- |
| 16    |

```sql
select avgValueIntegerSumTupleSketch(playerHomeRuns, 16) as value
from baseballStats 
```

| value |
| ----- |
| 12    |
