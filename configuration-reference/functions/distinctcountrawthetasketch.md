---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTRAWTHETASKETCH function.
---

# DISTINCTCOUNTRAWTHETASKETCH

The [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html) framework enables set operations over a stream of data, and can also be used for cardinality estimation. Pinot leverages the [Sketch Class](https://github.com/apache/incubator-datasketches-java/blob/master/src/main/java/org/apache/datasketches/theta/Sketch.java) and its extensions from the library `org.apache.datasketches:datasketches-java:1.2.0-incubating` to perform distinct counting as well as evaluating set operations.

## Signature

> DISTINCTCOUNTRAWTHETASKETCH(**\<thetaSketchColumn>, \<thetaSketchParams>, predicate1, predicate2..., postAggregationExpressionToEvaluate**) -> HexEncoded

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

| value                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AgMDAAAKzJOVAAAAAACAPwDAATjfLK5fBJQy2rIU1GYLOK5a09G+XQ1UHWt00/NwFTC4EwzexhE3CHBSU+YIUzkM0goIADEeFViAmzCRcx5FeHrMHfGsU/qrFvMP+Q87UYRC7LFzZ0FV3PIfAF1FMFsM+E9XRwZRYoR79VdK7z1jAD/WClziDmb4Cosm3ctidcRl9VxfNTR47OUFqFP4dYQkZwXIEZtEhngdkGfqkQCKZPX85HITAZrwVDpI4TY6paDTZwLQNiemHFCUlEZCKcOMpkXuYypOxjzXi1ES+07IIH7EqrQeKcssHvOUh2gpzIDajYdQ4UTS6IBoXPB6AtbomPBiMalFURDzh+xppzrg5HcUTMW4Iuzgv5Mz/xIm73yOe7seghzwmH+zXUfda/mkaBqU6XQEAQFagTkndhYHHcjLb0OeQg4BGDAHtRIDD8EqsonkilQT6TZq2uM3CRXJQTlaYewzFvHsKivVomgcQRojVnPKBh0d0GgYeF4eIEXtD1bZTw43eVR1Dk6sBj3pjleOW21dRsUCRmyEDGdIfWQVJXouaUnZqaC9gi1oSrG7GT8HO2xXeb32OzfiHVx5s9+5bGpFXoXTu1n7g2Jone8JMyGuam2x7Bt55a1JdtFCFxhZ2Gd7IajHY4lNBH2lDfUoJed4f7kGUEXmlU6BCfwOkJ1CIoWBTQY+NToDhpmmmPY+rVOH5coybBHlH4vpfPBbbQsOjl0YBSC9uEmZ3WubqnV0KZ1p5d7wq/F0p7Wgo8y4JVXAobKCB+hsVckBNIA4XrYMzdWVSWeQsXHSuR+mWmJPftadyrMlfvoy2mVr8R4Dih7k3XNhXZwjBeuNJQA5Dtci6w0uIUczvEL+nY+9CSHEPQhuT//aluJ2De4Fk94cfWgaxqhYyh10TTIWZFmsDxJeOMaPT1BCwVRF6taOjftNbVDC5Fy1BtVzVIIUOGeBcj5VbhHtqowIB1qGEDIJy9ZBXD73iFBN5kVgvicaFGSKHGQqeIVsgOFdcFKITQTuV2d0pkljkPXKUIc68M0KPpU6iZYuaBA4+hGR9nri0tVnbJZOM1Z/fi01ou5YLYCoHTqkImozpJMYXLCqKtTBm2o7sc5oQATXUBC9dqM8xQoGL8OmltUWc1cX35rtD2D2zHL2IncEKMzsN/c6S31W74VTBtcbJfP9rHENp7yO453qYhA7m++jl2MKFzdvtkHqGDUcs9FKisV9Hx+ruhaGsLkdISszkZ3sYykjx3NH6BbbaCZf9jTswuxHKheTbaEDmSgrx7BfK+Z2My4jdMqCrEtKMSuJqEJ22AM5U8MNFVkCPTobkCEdJx0ZQJu+Tk73t1v3nqLUQH4PbFJzcUrr9yZFZ0u+1mzNNQ5o0w+v1dSRLGsXsPyRqGkQchuz/DKyrjJzf9Vb8HY4Ni63XiaXwgJrjq9rgAp6EmWV2xXUOI9CWZa7HsuRWO95m58nIq9K8VCkO+T/rWwrPqZ/tCgEtkshqecNhszQiki0d5Kf26o/YcATx4ZkJ655y4PTVr+kY0Xbb/UwEo2pPd3Hyd4hVz1I5N9TpYaJk2Lok1+7N+3LG+3Lj3KZtd5/+j8RujEmogI= |

```sql
select distinctCountRawThetaSketch(teamID, 'nominalEntries=10') AS value
from baseballStats
```

| value                                                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AwMDAAAKzJMQAAAAAACAP4vpfPBbbQsO5N1zYV2cIwWFgU0GPjU6A4Z4HZBn6pEAyQE0gDhetgyKZPX85HITAQ4BGDAHtRIDEDub76OXYwoxK4moQnbYA9LogGhc8HoCE+k2atrjNwlVbhHtqowIBzd5VHUOTqwG+aRoGpTpdAT6PxG6MSaiAnshqMdjiU0EHEEaI1ZzygY= |

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
