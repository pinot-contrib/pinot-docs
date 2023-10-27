---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTRAWTHETASKETCH function.
---

# DISTINCTCOUNTRAWTHETASKETCH

The [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html) framework enables set operations over a stream of data, and can also be used for cardinality estimation. Pinot leverages the [Sketch Class](https://github.com/apache/datasketches-java/blob/master/src/main/java/org/apache/datasketches/theta/Sketch.java) and its extensions from the library `org.apache.datasketches:datasketches-java:4.2.0` to perform distinct counting as well as evaluating set operations.

## Signature

> distinctCountRawThetaSketch(**\<thetaSketchColumn>, \<thetaSketchParams>, predicate1, predicate2..., postAggregationExpressionToEvaluate**) -> HexEncoded

* `thetaSketchColumn` (required): Name of the column to aggregate on.
* `thetaSketchParams` (required): Parameters for constructing the intermediate theta-sketches.
  * Currently, the only supported parameter is `nominalEntries` (defaults to 4096).
* `predicates` (optional)\_: \_ These are individual predicates of form `lhs <op> rhs` which are applied on rows selected by the `where` clause. During intermediate sketch aggregation, sketches from the `thetaSketchColumn` that satisfies these predicates are unionized individually. For example, all filtered rows that match `country=USA` are unionized into a single sketch. Complex predicates that are created by combining (AND/OR) of individual predicates is supported.
* `postAggregationExpressionToEvaluate` (required)_:_ The set operation to perform on the individual intermediate sketches for each of the predicates. Currently supported operations are `SET_DIFF, SET_UNION, SET_INTERSECT` , where DIFF requires two arguments and the UNION/INTERSECT allow more than two arguments.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select distinctCountRawThetaSketch(teamID) AS value
from baseballStats 
```

| value                          |
| ------------------------------ |
| AgMDAAAKzJOVAAAAAACAPwDAATj... |

```sql
select distinctCountRawThetaSketch(teamID, 'nominalEntries=10') AS value
from baseballStats
```

| value                                       |
| ------------------------------------------- |
| AwMDAAAKzJMQAAAAAACAP4vpfPBbbQsO5N1zYV2c... |

We can also provide predicates and a post aggregation expression to compute more complicated cardinalities:

```sql
select distinctCountRawThetaSketch(
  yearID, 
  'nominalEntries=4096', 
  'teamID = ''SFN'' AND numberOfGames=28 AND homeRuns=1',
  'teamID = ''CHN'' AND numberOfGames=28 AND homeRuns=1',
  'SET_INTERSECT($1, $2)'
) AS value
from baseballStats 
```

| value                    |
| ------------------------ |
| AQMDAAA6zJN8QPYIsvHMNQ== |
