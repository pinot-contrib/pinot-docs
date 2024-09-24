---
description: >-
  This section contains reference documentation for the
	DISTINCTCOUNTRAWINTEGERSUMTUPLESKETCH function.
---

# DISTINCTCOUNTRAWINTEGERSUMTUPLESKETCH

The [Tuple Sketch](https://datasketches.apache.org/docs/Tuple/TupleOverview.html) is an extension of the [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html).  Tuple sketches store an additional summary value with each retained entry which makes the sketch ideal for summarizing attributes such as impressions or clicks.  Tuple sketches are interoperable with the Theta Sketch and enable set operations over a stream of data, and can also be used for cardinality estimation.

## Signature

> distinctCountRawIntegerSumTupleSketch(**\<tupleSketchColumn>, \<tupleSketchParams>**) -> HexEncoded

* `tupleSketchColumn` (required): Name of the column to aggregate on.  This must be an existing tuple sketch serialized as bytes.
* `tupleSketchParams` (required): Semicolon-separated parameter string for constructing the intermediate tuple-sketches.
  * The supported parameters are:
   * `nominalEntries`: The nominal entries used to create the sketch. (Default 65536)
   * `accumulatorThreshold`: How many sketches should be kept in memory before merging. (Default 2)

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

The `distinctCountRawIntegerSumTupleSketch` function can be used to extract the raw sketch encoded in hexadecimal form.  Only integer summaries are supported which are combined together using `sum` when two sketches have the same hashed key present in the retained items.

```sql
select distinctCountRawIntegerSumTupleSketch(playerHomeRuns) as value
from baseballStats 
```

| value                                       |
| ------------------------------------------- |
| AgMJAQAKzJONRAAAAAAAAAcADPv9ido0XwAAAAAP... |

```sql
select distinctCountRawIntegerSumTupleSketch(playerHomeRuns, 'nominalEntries=4096;accumulatorThreshold=10') as value
from baseballStats 
```

| value                                       |
| ------------------------------------------- |
| AwMJAQAKzJMQAAAAAAAAAK8pD3/6nBcAQWgQ6zI8... |

This function can also be used with the V2 query engine.
