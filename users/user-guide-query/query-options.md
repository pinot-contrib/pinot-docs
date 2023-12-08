---
description: This document contains all the available query options
---

# Query Options

## Supported Query Options

<table><thead><tr><th>Key</th><th width="249.33333333333331">Description</th><th>Default Behavior</th></tr></thead><tbody><tr><td><strong>timeoutMs</strong></td><td>Timeout of the query in milliseconds</td><td>Use table/broker level timeout</td></tr><tr><td><strong>enableNullHandling</strong></td><td>To enable basic null support (`IS NULL` and `IS NOT NULL`) and generate the null index, set **`nullHandlingEnabled=true`** in the Table index configuration ([tableIndexConfig](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1)). When null support is enabled, `IS NOT NULL` and `IS NULL` evaluate to `true` or `false` according to whether a null is detected. See (Null value support](../../../developers/advanced/null-value-support.md) for more information. (introduced in 0.11.0)</td><td><code>false</code> (disabled)</td></tr><tr><td><strong>explainPlanVerbose</strong></td><td>Return verbose result for <code>EXPLAIN</code> query (introduced in 0.11.0)</td><td><code>false</code> (not verbose)</td></tr><tr><td><strong>useMultistageEngine</strong></td><td>Use multi-stage engine to execute the query (introduced in 0.11.0)</td><td><code>false</code> (use single-stage engine)</td></tr><tr><td><strong>maxExecutionThreads</strong></td><td>Maximum threads to use to execute the query. Useful to limit the resource usage for expensive queries</td><td>Half of the CPU cores for non-group-by queries; all CPU cores for group-by queries</td></tr><tr><td><strong>numReplicaGroupsToQuery</strong></td><td>When replica-group based routing is enabled, use it to query multiple replica-groups (introduced in 0.11.0)</td><td><code>1</code> (only query servers within the same replica-group)</td></tr><tr><td><strong>minSegmentGroupTrimSize</strong></td><td>Minimum groups to keep when trimming groups at the segment level for group-by queries. See <a data-mention href="grouping-algorithm.md#configuration-parameters">#configuration-parameters</a></td><td>Server level config</td></tr><tr><td><strong>minServerGroupTrimSize</strong></td><td>Minimum groups to keep when trimming groups at the server level for group-by queries. See <a data-mention href="grouping-algorithm.md#configuration-parameters">#configuration-parameters</a></td><td>Server level config</td></tr><tr><td><strong>skipUpsert</strong></td><td>For upsert-enabled table, skip the effect of upsert and query all the records. See <a data-mention href="../../basics/data-import/upsert.md">upsert.md</a></td><td><code>false</code> (exclude the replaced records)</td></tr><tr><td><strong>useStarTree</strong></td><td>Useful to debug the star-tree index (introduced in 0.11.0)</td><td><code>true</code> (use star-tree if available)</td></tr><tr><td><strong>AndScanReordering</strong></td><td><a href="https://docs.pinot.apache.org/operators/tutorials/performance-optimization-configurations?q=andoperator">See detailed description</a></td><td>disabled</td></tr><tr><td><strong>maxRowsInJoin</strong></td><td>Configure maximum rows allowed in join hash-table creation phase</td><td><p>default value read from cluster config</p><pre><code>pinot.query.join.max.rows

</code></pre><p>if not set, the default will be</p><p><strong>2^20 (1024*1024)</strong></p></td></tr><tr><td><strong>inPredicatePreSorted</strong></td><td>(Only apply to STRING columns) Indicates that the values in the IN clause is already sorted, so that Pinot doesn't need to sort them again at query time</td><td><code>false</code> (values in IN predicate is not pre-sorted)</td></tr><tr><td><strong>inPredicateLookupAlgorithm</strong></td><td><p>(Only apply to STRING columns) The algorithm to use to look up the dictionary ids for the IN clause values.</p><ul><li><code>DIVIDE_BINARY_SEARCH</code>: Sort the IN clause values and do binary search on both dictionary and IN clause values at same time to reduce the value lookups</li></ul><ul><li><code>SCAN</code>: Sort the IN clause values and scan both dictionary and IN clause values to get the matching dictionary ids</li><li><code>PLAIN_BINARY_SEARCH</code>: Do not sort the IN clause values, but directly binary search each IN clause value in the dictionary</li></ul></td><td><code>DIVIDE_BINARY_SEARCH</code></td></tr></tbody></table>

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
