---
description: Learn how to implement a custom OpChain converter for multi-stage engine extensibility
---

# OpChain Converter Plugin

## Overview

The `OpChainConverter` SPI (Service Provider Interface) allows plugin developers to provide alternative implementations for converting logical query plans into executable OpChain objects in the multi-stage query engine. This enables extensibility for alternative execution backends, such as integrating specialized execution engines (e.g., timeseries engines) with Pinot's multi-stage execution (MSE).

## Why Use OpChain Converter SPI?

The OpChainConverter SPI is useful when you need to:

* Implement alternative plan-to-OpChain conversion logic for specific execution scenarios
* Integrate custom execution backends with the multi-stage engine
* Optimize query execution for specialized workloads or hardware
* Support alternative query execution strategies

## Implementing an OpChain Converter

To create a custom OpChain converter, implement the `OpChainConverter` interface:

```java
package org.apache.pinot.query.runtime.operator;

public interface OpChainConverter {
  /**
   * Converts a logical plan node into an OpChain for execution.
   *
   * @param context the plan request context containing query metadata
   * @param planNode the logical query plan node to convert
   * @return an OpChain ready for execution, or null if this converter cannot handle this plan
   */
  OpChain convert(PlanRequestContext context, PlanNode planNode);

  /**
   * Returns the priority of this converter. Higher priority converters are selected first.
   * When multiple converters have the same priority, they are ordered by converter ID.
   *
   * @return the priority value (higher = higher priority)
   */
  int priority();

  /**
   * Returns a unique identifier for this converter.
   *
   * @return the converter ID
   */
  String getId();
}
```

## Registering Your OpChain Converter

Once you've implemented the `OpChainConverter` interface, register it using Java's ServiceLoader mechanism:

1. Add the `@AutoService` annotation from Google's `com.google.auto:auto-service` library:

```java
import com.google.auto.service.AutoService;
import org.apache.pinot.query.runtime.operator.OpChainConverter;

@AutoService(OpChainConverter.class)
public class CustomOpChainConverter implements OpChainConverter {

  @Override
  public OpChain convert(PlanRequestContext context, PlanNode planNode) {
    // Implement your conversion logic here
    // Return null if this converter cannot handle the plan
    if (!canHandle(planNode)) {
      return null;
    }
    return convertToOpChain(context, planNode);
  }

  @Override
  public int priority() {
    return 100; // Set your converter's priority
  }

  @Override
  public String getId() {
    return "custom-converter";
  }

  private boolean canHandle(PlanNode planNode) {
    // Implement logic to determine if this converter can handle the plan
    return true;
  }

  private OpChain convertToOpChain(PlanRequestContext context, PlanNode planNode) {
    // Implement your conversion logic
    return null;
  }
}
```

2. Create a ServiceLoader configuration file at `META-INF/services/org.apache.pinot.query.runtime.operator.OpChainConverter` in your JAR:

```
com.example.CustomOpChainConverter
```

## Priority and Selection

The `OpChainConverterDispatcher` manages all registered converters and selects the active one based on:

1. **Priority**: Higher priority values are evaluated first
2. **Tie-breaking**: When multiple converters have the same priority, they are ordered by converter ID (alphabetically)
3. **Explicit override**: You can explicitly set the active converter using `OpChainConverterDispatcher.setActiveConverterIdOverride(String converterId)`

## Example: Custom Converter Implementation

Here's a complete example of a custom OpChain converter that handles specific plan node types:

```java
import com.google.auto.service.AutoService;
import org.apache.pinot.query.planner.PlanNode;
import org.apache.pinot.query.runtime.operator.OpChain;
import org.apache.pinot.query.runtime.operator.OpChainConverter;
import org.apache.pinot.query.runtime.plan.PlanRequestContext;

@AutoService(OpChainConverter.class)
public class TimeSeriesOpChainConverter implements OpChainConverter {
  private static final String CONVERTER_ID = "timeseries-converter";
  private static final int PRIORITY = 50;

  @Override
  public OpChain convert(PlanRequestContext context, PlanNode planNode) {
    // Check if this is a time-series query that we can optimize
    if (!isTimeSeriesQuery(planNode)) {
      return null;
    }

    // Perform custom conversion optimized for time-series execution
    return optimizeTimeSeriesExecution(context, planNode);
  }

  @Override
  public int priority() {
    return PRIORITY;
  }

  @Override
  public String getId() {
    return CONVERTER_ID;
  }

  private boolean isTimeSeriesQuery(PlanNode planNode) {
    // Implement logic to detect time-series queries
    // For example, check for time-based aggregations, windowing, etc.
    return false;
  }

  private OpChain optimizeTimeSeriesExecution(PlanRequestContext context, PlanNode planNode) {
    // Implement time-series-specific optimization logic
    return null;
  }
}
```

## Default Implementation

Pinot includes a `DefaultOpChainConverter` that delegates to the existing `PlanNodeToOpChain` converter. This converter has the lowest priority and serves as a fallback when no other converter can handle a query plan.

## Testing Your OpChain Converter

When testing your OpChain converter:

1. Ensure it properly implements the `OpChainConverter` interface
2. Test that it correctly handles the types of query plans it's designed for
3. Verify that returning `null` gracefully delegates to the next converter
4. Test priority-based selection when multiple converters are available
5. Verify explicit override functionality works correctly

## Related Documentation

* [Multi-stage query engine overview](../../../build-with-pinot/querying-and-sql/sse-vs-mse.md)
* [Plugin architecture](../README.md)
* [Using the multi-stage query engine](../../../build-with-pinot/querying-and-sql/sse-vs-mse.md)
