---
description: >-
  This page has a collection of frequently asked questions about queries with answers from the
  community.
---

# Query FAQ

{% hint style="info" %}
This is a list of questions frequently asked in our troubleshooting channel on Slack. To contribute additional questions and answers, [make a pull request](https://docs.pinot.apache.org/contributing/contributing).
{% endhint %}

## Querying

### I get the following error when running a query, what does it mean?

```json
{'errorCode': 410, 'message': 'BrokerResourceMissingError'}
```

This implies that the Pinot Broker assigned to the table specified in the query was not found. A common root cause for this is a typo in the table name in the query. Another uncommon reason could be if there wasn't actually a broker with required broker tenant tag for the table.

### What are all the fields in the Pinot query's JSON response?

See this page explaining the Pinot response format: [https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format](https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format).

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

For changing the timeout on the entire cluster, set this property `pinot.broker.timeoutMs`  in either broker configs or cluster configs (using the POST /cluster/configs API from Swagger).

### How do I cancel a query?

Add these two configs for Pinot server and broker to start tracking of running queries. The query tracks are added and cleaned as query starts and ends, so should not consume much resource.

```java
pinot.server.enable.query.cancellation=true // false by default
pinot.broker.enable.query.cancellation=true // false by default
```

Then use the Rest APIs on Pinot controller to list running queries and cancel them via the query ID and broker ID (as query ID is only local to broker), like in the following:

```json
GET /queries: to show running queries as tracked by all brokers
Response example: `{
  "Broker_192.168.0.105_8000": {
    "7": "select G_old from baseballStats limit 10",
    "8": "select G_old from baseballStats limit 100"
  }
}`

DELETE /query/{brokerId}/{queryId}[?verbose=false/true]: to cancel a running query 
with queryId and brokerId. The verbose is false by default, but if set to true, 
responses from servers running the query also return.

Response example: `Cancelled query: 8 with responses from servers: 
{192.168.0.105:7501=404, 192.168.0.105:7502=200, 192.168.0.105:7500=200}`
```

### How do I optimize my Pinot table for doing aggregations and group-by on high cardinality columns ?

In order to speed up aggregations, you can enable metrics aggregation on the required column by adding a [metric field](https://docs.pinot.apache.org/configuration-reference/schema#metricfieldspecs) in the corresponding schema and setting `aggregateMetrics` to true in the table configuration. You can also use a star-tree index config for columns like these ([see here for more about star-tree](https://docs.pinot.apache.org/basics/indexing/star-tree-index)).

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

