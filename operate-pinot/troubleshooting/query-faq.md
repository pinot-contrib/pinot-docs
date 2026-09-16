---
description: >-
  This page has a collection of frequently asked questions about queries with
  answers from the community.
---

# Query FAQ

{% hint style="info" %}
This is a list of questions frequently asked in our troubleshooting channel on Slack. To contribute additional questions and answers, [make a pull request](../../contributing/contributing.md).
{% endhint %}

## Querying

### I get the following error when running a query, what does it mean?

```json
{'errorCode': 410, 'message': 'BrokerResourceMissingError'}
```

Error code 410 (`BROKER_RESOURCE_MISSING`) means the broker handling the query has no routing entry for the table. Check the table name and whether the table is assigned to that broker's tenant. This can also occur temporarily while broker routing changes, such as during a table move between broker tenants or broker scale-down.

Both the single-stage and multi-stage query engines report code 410 for this condition. In older Pinot versions, the multi-stage engine could report the generic `INTERNAL` code 450 instead. A query whose segments are all filtered out is different: it returns an empty result, not this routing error.

If a client handles this condition, inspect the Pinot error code rather than relying on HTTP status alone. By default, query errors can be returned with HTTP 200 and the code in `X-Pinot-Error-Code`; with HTTP-status-for-errors enabled, this error maps to HTTP 503. See the [query response format](../../reference/api-reference/query-response-format.md) for the response's `exceptions` field.

### What are all the fields in the Pinot query's JSON response?

See this page explaining the Pinot response format: [docs](../../reference/api-reference/query-response-format.md).

### SQL Query fails with "Encountered 'timestamp' was expecting one of..."

"timestamp" is a reserved keyword in SQL. Escape timestamp with double quotes.

```sql
select "timestamp" from myTable
```

Other commonly encountered reserved keywords are date, time, table.

### Filtering on STRING column WHERE column = "foo" does not work?

For filtering on STRING columns, use single quotes:

```sql
SELECT COUNT(*) from myTable WHERE column = 'foo'
```

### ORDER BY using an alias doesn't work?

The fields in the `ORDER BY` clause must be one of the group by clauses or aggregations, _**BEFORE**_ applying the alias. Therefore, this will not work:

```sql
SELECT count(colA) as aliasA, colA from tableA GROUP BY colA ORDER BY aliasA
```

But, this will work:

```sql
SELECT count(colA) as sumA, colA from tableA GROUP BY colA ORDER BY count(colA)
```

### Does pagination work in GROUP BY queries?

No. Pagination only works for SELECTION queries.

### How do I increase timeout for a query ?

You can add this at the end of your query: `option(timeoutMs=X)`. Tthe following example uses a timeout of 20 seconds for the query:

```sql
SELECT COUNT(*) from myTable option(timeoutMs=20000)
```

You can also use `SET "timeoutMs" = 20000; SELECT COUNT(*) from myTable`.

For changing the timeout on the entire cluster, set this property `pinot.broker.timeoutMs` in either broker configs or cluster configs (using the POST /cluster/configs API from Swagger).

### How do I cancel a query?

See [query-cancellation.md](../../build-with-pinot/querying-and-sql/query-execution-controls/query-cancellation.md)

### How do I optimize my Pinot table for doing aggregations and group-by on high cardinality columns ?

In order to speed up aggregations, you can enable metrics aggregation on the required column by adding a [metric field](../../reference/configuration-reference/schema.md#metricfieldspecs) in the corresponding schema and setting `aggregateMetrics` to true in the table configuration. You can also use a star-tree index config for columns like these ([see here for more about star-tree](../../build-with-pinot/indexing/star-tree-index.md)).

### How do I verify that an index is created on a particular column ?

There are two ways to verify this:

1. Log in to a server that hosts segments of this table. Inside the data directory, locate the segment directory for this table. In this directory, there is a file named `index_map` which lists all the indexes and other data structures created for each segment. Verify that the requested index is present here.
2. During query: Use the column in the filter predicate and check the value of `numEntriesScannedInFilter`. If this value is 0, then indexing is working as expected (works for Inverted index).

### Does Pinot use a default value for LIMIT in queries?

Yes, Pinot uses a default value of `LIMIT 10` in queries. The reason behind this default value is to avoid unintentionally submitting expensive queries that end up fetching or processing a lot of data from Pinot. Users can always overwrite this by explicitly specifying a `LIMIT` value.

### Does Pinot cache query results?

Pinot does not cache query results. Each query is computed in its entirety. Note though, running the same or similar query multiple times will naturally pull in segment pages into memory making subsequent calls faster. Also, for real-time systems, the data is changing in real-time, so results cannot be cached. For offline-only systems, caching layer can be built on top of Pinot, with invalidation mechanism built-in to invalidate the cache when data is pushed into Pinot.

### I'm noticing that the first query is slower than subsequent queries. Why is that?

Pinot memory maps segments. It warms up during the first query, when segments are pulled into the memory by the OS. Subsequent queries will have the segment already loaded in memory, and hence will be faster. The OS is responsible for bringing the segments into memory, and also removing them in favor of other segments when other segments not already in memory are accessed.

### How do I determine if the star-tree index is being used for my query?

The query execution engine will prefer to use the star-tree index for all queries where it can be used. The criteria to determine whether the star-tree index can be used is as follows:

* All aggregation function + column pairs in the query must exist in the star-tree index.
* All dimensions that appear in filter predicates and group-by should be star-tree dimensions.

For queries where above is true, a star-tree index is used. For other queries, the execution engine will default to using the next best index available.
