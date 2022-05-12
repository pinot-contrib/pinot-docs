# Query FAQ

## Querying

### I get the following error when running a query, what does it mean?

```
{'errorCode': 410, 'message': 'BrokerResourceMissingError'}
```

This essentially implies that the Pinot Broker assigned to the table specified in the query was not found. A common root cause for this is a typo in the table name in the query. Another uncommon reason could be if there wasn't actually a broker with required broker tenant tag for the table.

### What are all the fields in the Pinot query's JSON response?

Here's the page explaining the Pinot response format: [https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format](https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format)

### SQL Query fails with "Encountered 'timestamp' was expecting one of..."

"timestamp" is a reserved keyword in SQL. Escape timestamp with double quotes.&#x20;

```
select "timestamp" from myTable
```

Other commonly encountered reserved keywords are date, time, table.

### Filtering on STRING column WHERE column = "foo" does not work?

For filtering on STRING columns, use single quotes

```
SELECT COUNT(*) from myTable WHERE column = 'foo'
```

### ORDER BY using an alias doesn't work?

The fields in the `ORDER BY` clause must be one of the group by clauses or aggregations, _**BEFORE**_ applying the alias. Therefore, this will not work

```
SELECT count(colA) as aliasA, colA from tableA GROUP BY colA ORDER BY aliasA
```

Instead, this will work

```
SELECT count(colA) as sumA, colA from tableA GROUP BY colA ORDER BY count(colA)
```

### Does pagination work in GROUP BY queries?

No. Pagination only works for SELECTION queries

### How do I increase timeout for a query ?

You can add this at the end of your query: `option(timeoutMs=X)`. For eg: the following example will use a timeout of 20 seconds for the query:

```
SELECT COUNT(*) from myTable option(timeoutMs=20000)
```

### How do I optimize my Pinot table for doing aggregations and group-by on high cardinality columns ?

In order to speed up aggregations, you can enable metrics aggregation on the required column by adding a [metric field](https://docs.pinot.apache.org/configuration-reference/schema#metricfieldspecs) in the corresponding schema and setting `aggregateMetrics` to true in the table config. You can also use a star-tree index config for such columns ([read more about star-tree here](https://docs.pinot.apache.org/basics/indexing/star-tree-index)) &#x20;

### How do I verify that an index is created on a particular column ?

There are 2 ways to verify this:

1. Log in to a server that hosts segments of this table. Inside the data directory, locate the segment directory for this table. In this directory, there is a file named `index_map` which lists all the indexes and other data structures created for each segment. Verify that the requested index is present here.
2. During query: Use the column in the filter predicate and check the value of `numEntriesScannedInFilter` . If this value is 0, then indexing is working as expected (works for Inverted index)

### Does Pinot use a default value for LIMIT in queries?

Yes, Pinot uses a default value of _LIMIT 10_ in queries. The reason behind this default value is to avoid unintentionally submitting expensive queries that end up fetching or processing a lot of data from Pinot. Users can always overwrite this by explicitly specifying a _LIMIT_ value.&#x20;

### Does Pinot cache query results?

Pinot does not cache query results, each query is computed in its entirety. Note though, running the same or similar query multiple times will naturally pull in segment pages into memory making subsequent calls faster. Also, for realtime systems, the data is changing in realtime, so results cannot be cached. For offline-only systems, caching layer can be built on top of Pinot, with invalidation mechanism built-in to invalidate the cache when data is pushed into Pinot.

### I'm noticing that the first query is slower than subsequent queries, why is that?

Pinot memory maps segments. It warms up during the first query, when segments are pulled into the memory by the OS. Subsequent queries will have the segment already loaded in memory, and hence will be faster. The OS is responsible for bringing the segments into memory, and also removing them in favor of other segments when other segments not already in memory are accessed.&#x20;

### How do I determine if StarTree index is being used for my query?

The query execution engine will prefer to use StarTree index for all queries where it can be used. The criteria to determine whether StarTree index can be used is as follows:

* All aggregation function + column pairs in the query must exist in the StarTree index.
* All dimensions that appear in filter predicates and group-by should be StarTree dimensions.

For queries where above is true, StarTree index is used. For other queries, the execution engine will default to using the next best index available.&#x20;

