---
description: This document contains all the available query options
---

# Query Options

## Supported Query Options

| Key                         | Description                                                                                                                                                                      | Default Behavior                                                                   |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **timeoutMs**               | Timeout of the query in milliseconds                                                                                                                                             | Use table/broker level timeout                                                     |
| **enableNullHandling**      | Enable the null handling of the query (introduced in 0.11.0)                                                                                                                     | `false` (disabled)                                                                 |
| **explainPlanVerbose**      | Return verbose result for `EXPLAIN` query (introduced in 0.11.0)                                                                                                                 | `false` (not verbose)                                                              |
| **useMultistageEngine**     | Use multi-stage engine to execute the query (introduced in 0.11.0)                                                                                                               | `false` (use single-stage engine)                                                  |
| **maxExecutionThreads**     | Maximum threads to use to execute the query. Useful to limit the resource usage for expensive queries                                                                            | Half of the CPU cores for non-group-by queries; all CPU cores for group-by queries |
| **numReplicaGroupsToQuery** | When replica-group based routing is enabled, use it to query multiple replica-groups (introduced in 0.11.0)                                                                      | `1` (only query servers within the same replica-group)                             |
| **minSegmentGroupTrimSize** | Minimum groups to keep when trimming groups at the segment level for group-by queries. See [#configuration-parameters](grouping-algorithm.md#configuration-parameters "mention") | Server level config                                                                |
| **minServerGroupTrimSize**  | Minimum groups to keep when trimming groups at the server level for group-by queries. See [#configuration-parameters](grouping-algorithm.md#configuration-parameters "mention")  | Server level config                                                                |
| **skipUpsert**              | For upsert-enabled table, skip the effect of upsert and query all the records. See [upsert.md](../../basics/data-import/upsert.md "mention")                                     | `false` (exclude the replaced records)                                             |
| **useStarTree**             | Useful to debug the star-tree index (introduced in 0.11.0)                                                                                                                       | `true` (use star-tree if available)                                                |
| **AndScanReordering**       | [See detailed description](https://docs.pinot.apache.org/operators/tutorials/performance-optimization-configurations?q=andoperator)                                              | disabled                                                                           |



## Set Query Options

### SET statement

After release 0.11.0, query options can be set using the `SET` statement:

```sql
SET key1 = 'value1';
SET key2 = 123;
SELECT * FROM myTable
```

### OPTION keyword (deprecated)

Before release 0.11.0, query options can be appended to the query with the `OPTION` keyword:

```sql
SELECT * FROM myTable OPTION(key1=value1, key2=123)
SELECT * FROM myTable OPTION(key1=value1) OPTION(key2=123)
SELECT * FROM myTable OPTION(timeoutMs=30000)
```
