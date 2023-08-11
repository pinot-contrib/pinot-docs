# Writing Custom Aggregation Function

Pinot has many built-in Aggregation Functions such as MIN, MAX, SUM, AVG etc. See [PQL](../../../users/user-guide-query/querying-pinot.md) page for the list of aggregation functions.

Adding a new AggregationFunction requires two things

* Implement [AggregationFunction](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/function/AggregationFunction.java) interface and make it available as part of the classpath
* Register the function in [AggregationFunctionFactory](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/function/AggregationFunctionFactory.java). As of today, this requires code change in Pinot but we plan to add the ability to plugin Functions without having to change Pinot code.

To get an overall idea, see [MAX](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/function/MaxAggregationFunction.java) Aggregation Function implementation. All other implementations can be found [here](https://github.com/apache/pinot/tree/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/function).

Lets look at the key methods to implements in AggregationFunction

```
interface AggregationFunction {

  AggregationResultHolder createAggregationResultHolder();

  GroupByResultHolder createGroupByResultHolder(int initialCapacity, int maxCapacity);

  void aggregate(int length, AggregationResultHolder aggregationResultHolder, Map<String, BlockValSet> blockValSetMap);

  void aggregateGroupBySV(int length, int[] groupKeyArray, GroupByResultHolder groupByResultHolder,
      Map<String, BlockValSet> blockValSets);

  void aggregateGroupByMV(int length, int[][] groupKeysArray, GroupByResultHolder groupByResultHolder,
      Map<String, BlockValSet> blockValSets);

  IntermediateResult extractAggregationResult(AggregationResultHolder aggregationResultHolder);

  IntermediateResult extractGroupByResult(GroupByResultHolder groupByResultHolder, int groupKey);

  IntermediateResult merge(IntermediateResult intermediateResult1, IntermediateResult intermediateResult2);

  FinalResult extractFinalResult(IntermediateResult intermediateResult);

}
```

Before getting into the implementation, it's important to understand how Aggregation works in Pinot.

This is advanced topic and assumes you know Pinot [concepts](../../../basics/concepts.md). All the data in Pinot is stored in segments across multiple nodes. The query plan at a high level comprises of 3 phases

**1. Map phase**

This phase works on the individual segments in Pinot.

* Initialization: Depending on the query type the following methods are invoked to set up the result holder.  While having different methods and return types adds complexity, it helps in performance.
  * AGGREGATION : `createAggregationResultHolder`This must return an instance of type [AggregationResultHolder](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/AggregationResultHolder.java). You can either use the [DoubleAggregationResultHolder](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/DoubleAggregationResultHolder.java) or [ObjectAggregationResultHolder](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/ObjectAggregationResultHolder.java)
  * GROUP BY: `createGroupByResultHolder`This method must return an instance of type [GroupByResultHolder](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/groupby/GroupByResultHolder.java). Depending on the type of result object, you might be able to use one of the existing [implementations](https://github.com/apache/pinot/tree/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/groupby).
*   Callback: For every record that matches the filter condition in the query,

    one of the following methods are invoked depending on the queryType(aggregation vs group by) and columnType(single-value vs multi-value). Note that we invoke this method for a batch of records instead of every row for performance reasons and allows JVM to vectorize some of parts of the execution if possible.

    * AGGREGATION: aggregate(int length, AggregationResultHolder aggregationResultHolder, Map\<String,BlockValSet> blockValSetMap)
      * **length**: This represent length of the block. Typically < 10k
      * **aggregationResultHolder**: this is the object returned from`createAggregationResultHolder`
      * **blockValSetMap**: Map of blockValSets depending on the arguments to the AggFunction
    * Group By Single Value: aggregateGroupBySV(int **length**, int\[] **groupKeyArray**, GroupByResultHolder **groupByResultHolder**, Map **blockValSets**)
      * **length:** This represent length of the block. Typically < 10k
      * **groupKeyArray:**  Pinot internally maintains a value to int mapping and this groupKeyArray maps to the internal mapping. These values together form a unique key.
      * **groupByResultHolder:** This is the object returned from`createGroupByResultHolder`
      * **blockValSetMap**: Map of blockValSets depending on the arguments to the AggFunction
    * Group By Multi Value: aggregateGroupBySV(int **length**, int\[] **groupKeyArray**, GroupByResultHolder **groupByResultHolder**, Map **blockValSets**)
      * **length:** This represent length of the block. Typically < 10k
      * **groupKeyArray:**  Pinot internally maintains a value to int mapping and this groupKeyArray maps to the internal mapping. These values together form a unique key.
      * **groupByResultHolder:** This is the object returned from`createGroupByResultHolder`
      * **blockValSetMap**: Map of blockValSets depending on the arguments to the AggFunction

**2. Combine phase**

In this phase, the results from all segments within a single pinot server are combined into IntermediateResult. The type of IntermediateResult is based on the Generic Type defined in the AggregationFunction implementation.

```
public interface AggregationFunction<IntermediateResult, FinalResult extends Comparable> {

  IntermediateResult merge(IntermediateResult intermediateResult1, IntermediateResult intermediateResult2);

}
```

**3. Reduce phase**

There are two steps in the Reduce Phase

* Merge all the IntermediateResult's from various servers using the  **merge** function
* Extract the final results by invoking the extractFinalResult method. In most cases, FinalResult is same type as IntermediateResult. [AverageAggregationFunction](https://github.com/apache/pinot/blob/master/pinot-core/src/main/java/org/apache/pinot/core/query/aggregation/function/AvgAggregationFunction.java) is an example where IntermediateResult (AvgPair) is different from FinalResult(Double)

```
  FinalResult extractFinalResult(IntermediateResult intermediateResult);
```
