# Query FAQ

## Querying

### What are all the fields in the Pinot query's JSON response?

Here's the page explaining the Pinot response format: [https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format](https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format)

### SQL Query fails with "Encountered 'timestamp' was expecting one of..."

"timestamp" is a reserved keyword in SQL. Escape timestamp with double quotes. 

```text
select "timestamp" from myTable
```

Other commonly encountered reserved keywords are date, time, table.

### Filtering on STRING column WHERE column = "foo" does not work?

For filtering on STRING columns, use single quotes

```text
SELECT COUNT(*) from myTable WHERE column = 'foo'
```

### ORDER BY using an alias doesn't work?

The fields in the `ORDER BY` clause must be one of the group by clauses or aggregations, _**BEFORE**_ applying the alias. Therefore, this will not work

```text
SELECT count(colA) as aliasA, colA from tableA GROUP BY colA ORDER BY aliasA
```

Instead, this will work

```text
SELECT count(colA) as sumA, colA from tableA GROUP BY colA ORDER BY count(colA)
```

### Does pagination work in GROUP BY queries?

No. Pagination only works for SELECTION queries

### How do I increase timeout for a query ?

You can add this at the end of your query: `option(timeoutMs=X)`. For eg: the following example will use a timeout of 20 seconds for the query:

```text
SELECT COUNT(*) from myTable option(timeoutMs=20000)
```

### How do I optimize my Pinot table for doing aggregations and group-by on high cardinality columns ?

In order to speed up aggregations, you can enable metrics aggregation on the required column by adding a [metric field](https://docs.pinot.apache.org/configuration-reference/schema#metricfieldspecs) in the corresponding schema and setting `aggregateMetrics` to true in the table config. You can also use a star-tree index config for such columns \([read more about star-tree here](https://docs.pinot.apache.org/basics/indexing/star-tree-index)\)  

