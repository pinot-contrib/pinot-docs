---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTTHETASKETCH
  function.
---

# DISTINCTCOUNTTHETASKETCH

The [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html) framework enables set operations over a stream of data, and can also be used for cardinality estimation. Pinot leverages the [Sketch Class](https://github.com/apache/datasketches-java/blob/master/src/main/java/org/apache/datasketches/theta/Sketch.java) and its extensions from the library `org.apache.datasketches:datasketches-java:4.2.0` to perform distinct counting as well as evaluating set operations.

## Signature

> distinctCountThetaSketch(**\<thetaSketchColumn>, \<thetaSketchParams>, predicate1, predicate2..., postAggregationExpressionToEvaluate**) -> Long

* `thetaSketchColumn` (required): Name of the column to aggregate on.
* `thetaSketchParams` (required): Semicolon-separated parameter string for constructing the intermediate theta-sketches.
  * The supported parameters are:
  * `nominalEntries`: The nominal entries used to create the sketch. (Default 4096)
  * `samplingProbability`: Sets the upfront uniform sampling probability, p. (Default 1.0)
  * `accumulatorThreshold`: How many sketches should be kept in memory before merging. (Default 2)
* `predicates` (optional)\_: \_ These are individual predicates of form `lhs <op> rhs` which are applied on rows selected by the `where` clause. During intermediate sketch aggregation, sketches from the `thetaSketchColumn` that satisfies these predicates are unionized individually. For example, all filtered rows that match `country=USA` are unionized into a single sketch. Complex predicates that are created by combining (AND/OR) of individual predicates is supported.
* `postAggregationExpressionToEvaluate` (required)_:_ The set operation to perform on the individual intermediate sketches for each of the predicates. Currently supported operations are `SET_DIFF, SET_UNION, SET_INTERSECT` , where DIFF requires two arguments and the UNION/INTERSECT allow more than two arguments.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select distinctCountThetaSketch(teamID) AS value
from baseballStats 
```

| value |
| ----- |
| 149   |

```sql
select distinctCountThetaSketch(teamID, 'nominalEntries=10') AS value
from baseballStats
```

| value |
| ----- |
| 146   |

We can also provide predicates and a post aggregation expression to compute more complicated cardinalities. For example, we could can find the intersection of the following queries:

```sql
select yearID
from baseballStats
where teamID = 'SFN' AND numberOfGames = 28 AND homeRuns = 1
```

| yearID |
| ------ |
| 1986   |
| 1985   |

```sql
select yearID
from baseballStats
where teamID = 'CHN' AND numberOfGames = 28 AND homeRuns = 1
```

| yearID |
| ------ |
| 1937   |
| 2003   |
| 1979   |
| 1900   |
| 1986   |
| 1978   |
| 2012   |

(the yearId `1986` is the only one in common)

By running the following query:

```sql
select distinctCountThetaSketch(
  yearID, 
  'nominalEntries=4096', 
  'teamID = ''SFN'' AND numberOfGames=28 AND homeRuns=1',
  'teamID = ''CHN'' AND numberOfGames=28 AND homeRuns=1',
  'SET_INTERSECT($1, $2)'
) AS value
from baseballStats 
```

| value |
| ----- |
| 1     |
