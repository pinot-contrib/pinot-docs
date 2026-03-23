---
description: >-
  Describes how you can support custom or novel Time Series Query Languages like
  PromQL, M3QL, etc.
---

# Time Series Language Plugin

## Overview

Time Series Query Languages like PromQL, though limited in what they can do, are quite convenient for Time Series analysis. There are many Time Series Query Languages out there, and Pinot should be able to support any of them via its Time Series Language Plugin.

## Plugin High Level Design

We have a dedicated SPI for implementing the Time Series Plugin: [`pinot-timeseries-spi`](https://github.com/apache/pinot/tree/master/pinot-timeseries/pinot-timeseries-spi) .

To build support for your own language, you need to implement the following key components:

* `TimeSeriesLogicalPlanner` takes in a Time Series Request, and is expected to return a Plan Tree consisting of `BaseTimeSeriesPlanNode`. The leaves of the plan tree should be `LeafTimeSeriesPlanNode`. The planner can also define the `TimeBuckets` as it sees fit.
* `BaseTimeSeriesPlanNode` allows you to implement your own plan nodes. Each plan node is expected to return a `BaseTimeSeriesOperator` via its `run` method.
* `BaseTimeSeriesOperator` allows you to define and implement your operators.
* `BaseTimeSeriesBuilder` can be implemented for each aggregation type you want to support.

There is an example Plugin implementation in the apache/pinot repo under [pinot-plugins/pinot-timeseries-lang](https://github.com/apache/pinot/tree/master/pinot-plugins/pinot-timeseries-lang).

## Plugin Implementation Tips

* Consider using frameworks like JavaCC for implementing your Query Parser.
* `TimeBuckets` that you return from your planner can spill beyond the \[start, end] of the original request. You can also define the resolution based on your language's semantics.
* Choose the resolution of `TimeBuckets` wisely. Setting a very fine resolution can make your visualization tool slow or incur a lot of Heap in Pinot.
* Use the `limit` in the `LeafTimeSeriesPlanNode` to control the maximum number of series that can be returned from the leaf stage.
* Note that for each series returned by the Leaf Operator, there will be a `Double[]` array with length that is the same as `TimeBuckets#getTimeBuckets()` . Ideally you should tune your `limit` and the resolution of `TimeBuckets` based on a fixed upper-bound of the number of data points you want to allow.

## Related pages

* [Write Custom Plugins](./) -- how to package and deploy plugins
* [Plugin Architecture](../README.md) -- overview of all plugin families including time series language
