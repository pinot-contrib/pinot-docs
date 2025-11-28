# Time Series Queries

Pinot has a "Time Series Engine" that can be used to support any Time Series Query Language, provided an appropriate Time Series Language Plugin is implemented.

Languages such as PromQL, Uber's M3QL, and many more can be implemented using the Plugin. A toy language plugin, intended only for demo/testing purposes, is included in the apache/pinot repo.

## Running Time Series Queries with Quickstart

You can use the `time_series` Quickstart type to run Pinot with the Time Series Engine enabled. The Quickstart uses the toy language implementation included in the apache/pinot repo.

You can refer to our [Quick Start Examples](../../basics/getting-started/quick-start.md) page for more information.

## Running Time Series Queries in Production

Assuming you have implemented your own Timeseries Language Plugin, with the code-name "mytsql", you can set the following configurations in each of Controller, Broker and Server configs. The class and series builder factory names are hypothetical. Note that the key of the planner and series builder configs contain the language code.

```properties
pinot.timeseries.languages=mytsql
pinot.timeseries.mytsql.logical.planner.class=com.example.mytsql.MyTSLogicalPlanner
pinot.timeseries.mytsql.series.builder.factory=com.example.mytsql.MyTSQLSeriesBuilderFactory
```

Pinot even allows running multiple Time Series Query Languages. For instance, if you had another query language plugin for `promql` and you wanted to run it alongside `mytsql`, the configs would look like:

```properties
pinot.timeseries.languages=mytsql,promql
pinot.timeseries.mytsql.logical.planner.class=com.example.mytsql.MyTSLogicalPlanner
pinot.timeseries.mytsql.series.builder.factory=com.example.mytsql.MyTSQLSeriesBuilderFactory
pinot.timeseries.promql.logical.planner.class=com.example.promql.PromQLLogicalPlanner
pinot.timeseries.promql.series.builder.factory=com.example.promql.PromQLSeriesBuilderFactory
```
