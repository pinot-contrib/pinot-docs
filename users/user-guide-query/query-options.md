---
description: This document contains all the available query options
---

# Query Options

## Supported Query Options

<table><thead><tr><th>Key</th><th width="249.33333333333331">Description</th><th>Default Behavior</th></tr></thead><tbody><tr><td><strong>timeoutMs</strong></td><td>Timeout of the query in milliseconds</td><td>Use table/broker level timeout</td></tr><tr><td><strong>enableNullHandling</strong></td><td>Enables advanced null handling. See <a href="../../developers/advanced/null-value-support.md">Null value support</a> for more information.(introduced in 0.11.0)</td><td><code>false</code> (disabled)</td></tr><tr><td><strong>explainPlanVerbose</strong></td><td>Return verbose result for <code>EXPLAIN</code> query (introduced in 0.11.0)</td><td><code>false</code> (not verbose)</td></tr><tr><td><strong>useMultistageEngine</strong></td><td>Use multi-stage engine to execute the query (introduced in 0.11.0)</td><td><code>false</code> (use single-stage engine)</td></tr><tr><td><strong>maxExecutionThreads</strong></td><td>Maximum threads to use to execute the query. Useful to limit the resource usage for expensive queries</td><td>Half of the CPU cores for non-group-by queries; all CPU cores for group-by queries</td></tr><tr><td><strong>numReplicaGroupsToQuery</strong></td><td>When replica-group based routing is enabled, use it to query multiple replica-groups (introduced in 0.11.0)</td><td><code>1</code> (only query servers within the same replica-group)</td></tr><tr><td><strong>minSegmentGroupTrimSize</strong></td><td>Minimum groups to keep when trimming groups at the segment level for group-by queries. See <a data-mention href="grouping-algorithm.md#configuration-parameters">#configuration-parameters</a></td><td>Server level config</td></tr><tr><td><strong>minServerGroupTrimSize</strong></td><td>Minimum groups to keep when trimming groups at the server level for group-by queries. See <a data-mention href="grouping-algorithm.md#configuration-parameters">#configuration-parameters</a></td><td>Server level config</td></tr><tr><td><strong>serverReturnFinalResult</strong></td><td>For aggregation and group-by queries, ask servers to directly return final results instead of intermediate results for aggregations.<br>Can be applied when the group key is server partitioned, i.e. the column(s) is partitioned, and all the data for a partition is served by the same server.</td><td><code>true</code> when a single server is queried, <code>false</code> otherwise</td></tr><tr><td><strong>serverReturnFinalResultKeyUnpartitioned</strong></td><td>For group-by queries, ask servers to directly return final results instead of intermediate results for aggregations.<br>Different from <strong>serverReturnFinalResult</strong>, this option should be used when the group key is not server partitioned, but the aggregated column is server partitioned. It is particularly useful for distinct count queries.<br>When this option is enabled, server will return final results, but won't directly trim the result to the query limit.</td><td><code>false</code></td></tr><tr><td><strong>skipIndexes</strong></td><td><p>Which indexes to skip usage of (i.e. scan instead), per-column. This is useful for side-by-side comparison/debugging. There can be cases where the use of an index is actually more expensive than performing a scan of the docs which match other filters. One such example could be a low-selectivity inverted index used in conjunction with another highly selective filter.</p><p>Config can be specified using url parameter format: <code>skipIndexes='col1=inverted,range&#x26;col2=inverted'</code></p><p>Possible index types to skip are: <code>sorted, range, inverted, H3</code>. To find out which indexes are used to resolve a given query, use the <code>EXPLAIN</code> query.</p></td><td><code>null/empty</code> (use all available indexes)</td></tr><tr><td><strong>skipPlannerRules</strong></td><td><p>Which defaultly enabled query planner rules should be disabled. This is useful when <code>EXPLAIN PLAN FOR</code> suggests a rule evaluation is taking too long or when it is known that a rule produces sub-optimal plan for the query. Currently this only applies to rules in optProgram that are mostly logical transformations. </p><p>Config can be specified using rule names delimited by comma: <code>skipPlannerRules='FilterProjectTranspose,PruneEmptySort'</code></p><p>The rule name used here is consistent with the output of <code>EXPLAIN PLAN FOR</code>, which is the rule description.</p></td><td><code>null/empty</code> (no defaultly enabled rules are skipped)</td></tr><tr><td><strong>usePlannerRules</strong></td><td><p>Which query planner rules that are disabled by default should be used. This is useful when the defaultly disabled rules could help query execution.</p><p>Config can be specified using rule names delimited by comma: <code>usePlannerRules='AggregateJoinTransposeExtended,JoinToEnrichedJoin'</code>. This query option only applies to the set of defaultly disabled rules listed in <a data-mention href="default-disabled-rules.md">#default-disabled-rules</a></p><p>At this point, Pinot does not have a cost-based optimizer and the multi-stage query engine uses Calcite's HepPlanner for query optimization. The rules that are disabled by default are those that are only helpful under certain circumstances. For a more detailed description on what these rules do and when are they helpful, please see <a data-mention href="default-disabled-rules.md">#default-disabled-rules</a>.</p></td><td><code>null/empty</code> (no defaultly disabled rules are used)</td></tr><tr><td><strong>skipUpsert</strong></td><td>For upsert-enabled table, skip the effect of upsert and query all the records. See <a data-mention href="../../manage-data/data-import/upsert-and-dedup/upsert.md">upsert.md</a></td><td><code>false</code> (exclude the replaced records)</td></tr><tr><td><strong>useStarTree</strong></td><td>Useful to debug the star-tree index (introduced in 0.11.0)</td><td><code>true</code> (use star-tree if available)</td></tr><tr><td><strong>AndScanReordering</strong></td><td><a href="https://docs.pinot.apache.org/operators/tutorials/performance-optimization-configurations?q=andoperator">See detailed description</a></td><td>disabled</td></tr><tr><td><strong>maxRowsInJoin</strong></td><td>Configure maximum rows allowed in a join operation. This limit is applied to both the hash table build phase for the join's right input as well as the number of joined rows emitted after matching with the join's left input.</td><td><p>default value read from cluster config</p><pre><code>pinot.query.join.max.rows
</code></pre><p>if not set, the default will be</p><p><strong>2^20 (1024*1024)</strong></p></td></tr><tr><td><strong>inPredicatePreSorted</strong></td><td>(Only apply to STRING columns) Indicates that the values in the IN clause is already sorted, so that Pinot doesn't need to sort them again at query time</td><td><code>false</code> (values in IN predicate is not pre-sorted)</td></tr><tr><td><strong>inPredicateLookupAlgorithm</strong></td><td><p>(Only apply to STRING columns) The algorithm 
to use to look up the dictionary ids for the IN clause values.</p><ul><li><code>DIVIDE_BINARY_SEARCH</code>: Sort the IN clause values and do binary search on both dictionary and IN clause values at same time to reduce the value lookups</li></ul><ul><li><code>SCAN</code>: Sort the IN clause values and scan both dictionary and IN clause values to get the matching dictionary ids</li><li><code>PLAIN_BINARY_SEARCH</code>: Do not sort the IN clause values, but directly binary search each IN 
clause value in the dictionary</li></ul></td><td><code>DIVIDE_BINARY_SEARCH</code></td></tr><tr><td><strong>maxServerResponseSizeBytes</strong></td><td>Long value config indicating the maximum length of the serialized response per server for a query.</td><td><p>Overriding priortiy order:<br>1. QueryOption -> maxServerResponseSizeBytes</p><p>2. QueryOption -> maxQueryResponseSizeBytes</p><p>3. TableConfig -> maxServerResponseSizeBytes</p><p>4. TableConfig -> maxQueryResponseSizeBytes</p><p>5. 
BrokerConfig -> maxServerResponseSizeBytes</p><p>6. BrokerConfig -> maxServerResponseSizeBytes</p></td></tr><tr><td><strong>maxQueryResponseSizeBytes</strong></td><td>Long value config indicating the maximum serialized response size across all servers for a query. This value is equally divided across all servers processing the query.</td><td><p>Overriding priortiy order:<br>1. QueryOption -> maxServerResponseSizeBytes</p><p>2. QueryOption -> maxQueryResponseSizeBytes</p><p>3. TableConfig -> 
maxServerResponseSizeBytes</p><p>4. TableConfig -> maxQueryResponseSizeBytes</p><p>5. BrokerConfig -> maxServerResponseSizeBytes</p><p>6. BrokerConfig -> maxServerResponseSizeBytes</p></td></tr><tr><td><strong>filteredAggregationsSkipEmptyGroups</strong></td><td>This config can be set to <code>true</code> to avoid computing all the groups in a group by query with only filtered aggregations (and no non-filtered aggregations). By default, the groups are computed over all the rows returned by 
the main filter, even if certain rows will never match any of the aggregation filters. This is the standard SQL behavior. However, if the selectivity of the main filter is very high as compared to the selectivity of the aggregation filters, this query option can help provide a big performance boost if the empty groups aren't required. For instance, a query like <code>SELECT SUM(X) FILTER (WHERE Y = 1) FROM mytable</code> will compute the groups over all the rows in the table by default since 
there's no main query filter. Setting this query option to <code>true</code> in such cases can massively improve performance if there's an inverted index on column <code>Y</code> for instance.</td><td><code>false</code> (i.e., all groups are computed by default as per standard SQL)</td></tr><tr><td><strong>dropResults</strong></td><td>Set dropResults=true in the config to drop the resultTable from the response. Use this option to troubleshoot a customer's query (which may have sensitive data 
in the result) using metadata only.</td><td><code>false</code></td></tr><tr><td><strong>skipUnavailableServers</strong></td><td>Set skipUnavailableServers=true in the config to continue sending queries to remaining servers if dispatching a query fails.</td><td><code>false</code></td></tr><tr><td><strong>clientQueryId</strong></td><td>Set to define a <a href="query-correlation-id.md">custom correlation ID</a> for a query and to <a href="query-cancellation.md">cancel queries</a>.
</td><td><code>null/empty</code></td></tr></tbody><tr><td><strong>accurateGroupByWithoutOrderBy</strong></td><td>Improves correctness of group-by queries with LIMIT but without ORDER BY by applying better trimming on servers. See PR #15844. Set <code>accurateGroupByWithoutOrderBy=true</code> to enable</td><td><code>false</code> (disabled)</td></tr><tr><td><strong>traceRuleProductions</strong></td><td>Trace planner rule productions. Specify <code>SET traceRuleProductions=true</code> to collect 
and return 
planner rules that successfully produced new relations and the relation subtree before and after the production in time order along with rule attempt timing. Useful for debugging query planning.</td><td><code>false</code></td></tr></table>

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

### REST API

Query options can be specified in API using queryOptions as key and **';'** separated key-value pairs.\
Alternatively, we can also use the SET keyword in the sql query.

* [Using Controller Admin API](../api/pinot-rest-admin-interface.md)

```bash
curl -X POST 'http://localhost:9000/sql' \
-d '{
  "sql": "SELECT * FROM myTable",
  "trace": false,
  "queryOptions":"key1=value1;key2=123"
}'
```

* [Using Broker Query API](../api/querying-pinot-using-standard-sql/)

```bash
curl -X POST 'http://localhost:8099/query/sql' \
-d '{
  "sql": "SELECT * FROM myTable;",
  "trace": false,
  "queryOptions":"key1=value1;key2=123"
}'
```
