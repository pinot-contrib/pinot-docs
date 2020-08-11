---
description: Learn how to query Pinot using PQL
---

# Pinot Query Language \(PQL\)

## PQL

PQL is a derivative of SQL that supports selection, projection, aggregation, and grouping aggregation. 

## PQL Limitations

PQL is only a derivative of SQL, and it does not support Joins nor Subqueries. In order to support them, we suggest to rely on PrestoDB [https://prestodb.io/](https://prestodb.io/), although Subqueries are not completely supported by PrestoDB at the moment of writing. Refer [Presto](../../integrations/presto.md) for details on integration.

## PQL Examples

The Pinot Query Language \(PQL\) is very similar to standard SQL:

```sql
SELECT COUNT(*) FROM myTable
```

### Aggregation

```sql
SELECT COUNT(*), MAX(foo), SUM(bar) FROM myTable
```

### Grouping on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM myTable
  GROUP BY bar, baz LIMIT 50
```

### Ordering on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM myTable
  GROUP BY bar, baz 
  ORDER BY bar, MAX(foo) DESC LIMIT 50
```

### Filtering

```sql
SELECT COUNT(*) FROM myTable
  WHERE foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

### Selection \(Projection\)

```sql
SELECT * FROM myTable
  WHERE quux < 5
  LIMIT 50
```

### Ordering on Selection

```sql
SELECT foo, bar FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 100
```

### Pagination on Selection

Note: results might not be consistent if column ordered by has same value in multiple rows.

```sql
SELECT foo, bar FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 50, 100
```

### Wild-card match \(in WHERE clause only\)

To count rows where the column `airlineName` starts with `U`

```sql
SELECT count(*) FROM SomeTable
  WHERE regexp_like(airlineName, '^U.*')
  GROUP BY airlineName TOP 10
```

### UDF

As of now, functions have to be implemented within Pinot. Injecting functions is not allowed yet. The example below demonstrate the use of UDFs. More examples in [Transform Function in Aggregation Grouping](https://docs.pinot.apache.org/users/user-guide-query/pinot-query-language#transform-function-in-aggregation-and-grouping)

```sql
SELECT count(*) FROM myTable
  GROUP BY dateTimeConvert(timeColumnName, '1:MILLISECONDS:EPOCH', '1:HOURS:EPOCH', '1:HOURS')
```

### BYTES column

Pinot supports queries on BYTES column using HEX string. The query response also uses hex string to represent bytes value.

E.g. the query below fetches all the rows for a given UID.

```sql
SELECT * FROM myTable
  WHERE UID = "c8b3bce0b378fc5ce8067fc271a34892"
```

## PQL Specification

### SELECT

The select statement is as follows

```sql
SELECT <outputColumn> (, outputColumn, outputColumn,...)
  FROM <tableName>
  (WHERE ... | GROUP BY ... | ORDER BY ... | TOP ... | LIMIT ...)
```

`outputColumn` can be `*` to project all columns, columns \(`foo`, `bar`, `baz`\) or aggregation functions like \(`MIN(foo)`, `MAX(bar)`, `AVG(baz)`\).

### WHERE

Supported predicates are comparisons with a constant using the standard SQL operators \(`=`, `<`, `<=`, `>`, `>=`, `<>`, ‘!=’\) , range comparisons using `BETWEEN` \(`foo BETWEEN 42 AND 69`\), set membership \(`foo IN (1, 2, 4, 8)`\) and exclusion \(`foo NOT IN (1, 2, 4, 8)`\). For `BETWEEN`, the range is inclusive.

Comparison with a regular expression is supported using the regexp\_like function, as in `WHERE regexp_like(columnName, 'regular expression')`

### Filter Functions on Single Value/Multi-value 

* `EQUALS`
* `IN`
* `NOT IN`
* `GT`
* `LT`
* `BETWEEN`
* `REGEXP_LIKE`

For Multi-Valued columns, `EQUALS` is similar to `CONTAINS`. 

### GROUP BY

The `GROUP BY` clause groups aggregation results by a list of columns, or transform functions on columns \(see below\)

### ORDER BY

The `ORDER BY` clause orders selection results or group by results by a list of columns. PQL supports ordering `DESC` or `ASC`.

### TOP \(Deprecated\)

Deprecated in SQL syntax.

The `TOP n` clause causes the ‘n’ largest group results to be returned. If not specified, the top 10 groups are returned.

### LIMIT

The `LIMIT n` clause causes the selection results to contain at most ‘n’ results. The `LIMIT a, b` clause paginate the selection results from the ‘a’ th results and return at most ‘b’ results. By default, 10 records are returned in the result.

## Differences with SQL

{% hint style="warning" %}
These differences only apply to the PQL endpoint. They do not hold true for the standard-SQL endpoint, which is the recommended endpoint. More information about the two types of endpoints in [Querying Pinot](../api/querying-pinot-using-standard-sql/#rest-api-on-the-broker)
{% endhint %}

* `TOP` works like `LIMIT` for truncation in group by queries
* No need to select the columns to group with. The following two queries are both supported in PQL, where the non-aggregation columns are ignored.

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM mytable
  GROUP BY bar, baz
  TOP 50

SELECT bar, baz, MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM mytable
  GROUP BY bar, baz
  TOP 50
```

* The results will always order by the aggregated value \(descending\). The results for query

```sql
SELECT MIN(foo), MAX(foo) FROM myTable
  GROUP BY bar
  TOP 50
```

will be the same as the combining results from the following queries

```sql
SELECT MIN(foo) FROM myTable
  GROUP BY bar
  TOP 50
SELECT MAX(foo) FROM myTable
  GROUP BY bar
  TOP 50
```

where we don’t put the results for the same group together.

* No support for ORDER BY in aggregation group by. However, ORDER BY support was added recently and is available in the standard-SQL endpoint. It can be used in the PQL endpoint by passing `queryOptions` into the payload as follows

```javascript
{
  "pql" : "SELECT SUM(foo), SUM(bar) from myTable GROUP BY moo ORDER BY SUM(bar) ASC, moo DESC TOP 10",
  "queryOptions" : "groupByMode=sql;responseFormat=sql"
}
```

where,

* `groupByMode=sql` - standard sql way of execution group by, hence accepting order by
* `responseFormat=sql` - standard sql way of displaying results, in a tabular manner

