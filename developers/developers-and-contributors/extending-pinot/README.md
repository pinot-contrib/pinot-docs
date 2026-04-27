# Extending Pinot

This section covers how to extend Apache Pinot by writing custom code that plugs into Pinot's internal extension points. Use these extension points when you need behavior that goes beyond what the plugin system offers, such as adding a new aggregation function or a custom segment fetcher.

## When to extend vs. when to write a plugin

Pinot has two levels of extensibility:

| Approach | What it is | When to use |
|----------|-----------|-------------|
| **Extension point** (this section) | Custom code compiled into Pinot or loaded on the classpath. Requires changes to Pinot core or registration in a factory class. | You need a new aggregation function, a new segment fetcher protocol, or a UDF that is not available as a plugin SPI. |
| **Plugin** (plugin architecture) | A self-contained JAR loaded from the `/plugins` directory at startup. Uses Pinot's SPI interfaces and does not require changes to Pinot core. | You need a new input format, filesystem backend, stream connector, metrics library, or other capability covered by the plugin SPI. |

If a plugin SPI exists for your use case, prefer the plugin approach because it does not require modifying Pinot source code and is easier to maintain across upgrades. Use the extension-point approach only when no plugin SPI covers your requirement.

## Available extension points

### Custom aggregation functions

Pinot ships with built-in aggregation functions (MIN, MAX, SUM, AVG, and many more), but you can add your own by implementing the `AggregationFunction` interface and registering it in `AggregationFunctionFactory`.

A custom aggregation function must handle three query phases:

1. **Map** -- process individual segments and accumulate partial results
2. **Combine** -- merge partial results from segments on the same server
3. **Reduce** -- merge results across servers and extract the final value

See [Writing Custom Aggregation Functions](custom-aggregation-function.md) for the full interface, method-by-method walkthrough, and code pointers.

### Segment fetchers

When segments are produced by external systems (Hadoop, Spark, Flink), Pinot needs to fetch them from the location where they were written. Out of the box, Pinot supports HTTP/HTTPS and NFS. If your segments live in HDFS, S3, or another storage system, you can either configure a built-in fetcher or implement the `SegmentFetcher` interface for a custom protocol.

See [Segment Fetchers](segment-fetchers.md) for HDFS configuration, custom fetcher implementation, and push examples.

### Scalar functions and UDFs

Pinot supports user-defined scalar functions (UDFs) that can be used in SQL queries. Scalar functions are annotated with `@ScalarFunction` and registered automatically via the classpath. Unlike aggregation functions, scalar functions operate row-by-row and do not require merge logic.

See the [Pinot source code for ScalarFunction](https://github.com/apache/pinot/tree/master/pinot-common/src/main/java/org/apache/pinot/common/function/scalar) for built-in examples.

### Transform functions

Transform functions run during query execution to compute derived values on the fly. They implement the `TransformFunction` interface and are registered in `TransformFunctionFactory`. Custom transform functions are useful when you need server-side computation that is not expressible as a UDF.

## Prerequisites

Before extending Pinot, make sure you have:

* A local Pinot development environment set up (see [Dev Environment Setup](../code-setup.md))
* Familiarity with Pinot's [architecture and components](../../../basics/concepts/)
* Java 21+ and Maven for building
