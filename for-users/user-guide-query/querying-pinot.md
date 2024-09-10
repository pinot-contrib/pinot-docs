---
description: Learn how to query Pinot using SQL
---

# Querying Pinot

## SQL Interface

Pinot provides a SQL interface for querying, which uses the **Calcite SQL** parser to parse queries and the **MYSQL\_ANSI** dialect. For details on the syntax, see the the [Calcite documentation](https://calcite.apache.org/docs/reference.html). To find supported SQL operators, see [Class SqlLibraryOperators](https://calcite.apache.org/javadocAggregate/org/apache/calcite/sql/fun/SqlLibraryOperators.html).

## Pinot 1.0

In Pinot 1.0, the multi-stage query engine supports inner join, left-outer, semi-join, and nested queries out of the box. It's optimized for in-memory process and latency. For more information, see how to [enable and use the multi-stage query engine](../../for-developers/advanced/v2-multi-stage-query-engine.md).

Pinot also supports using simple Data Definition Language (DDL) to insert data into a table from file directly. For details, see [programmatically access the multi-stage query engine](../../for-developers/advanced/v2-multi-stage-query-engine.md#programmatically-access-the-multi-stage-query-engine). More DDL supports will be added in the future. But for now, the most common way for data definition is using the [Controller Admin API](https://docs.pinot.apache.org/users/api/pinot-rest-admin-interface).

{% hint style="info" %}
**Note:** For queries that require a large amount of data shuffling, require spill-to-disk, or are hitting any other limitations of the multi-stage query engine (v2), we still recommend using **Presto**.
{% endhint %}

## Identifier vs Literal

In Pinot SQL:

* **Double quotes(")** are used to force string identifiers, e.g. column names
* **Single quotes(')** are used to enclose string literals. If the string literal also contains a single quote, escape this with a single quote e.g `'''Pinot'''` to match the string literal `'Pinot'`

Misusing those might cause unexpected query results, like the following examples:

* `WHERE a='b'` means the predicate on the column `a` equals to a string literal value `'b'`
* `WHERE a="b"` means the predicate on the column `a` equals to the value of the column `b`

If your column names use reserved keywords (e.g. `timestamp` or `date`) or special characters, you will need to use double quotes when referring to them in queries.

Note: Define decimal literals within quotes to preserve precision.

## Example Queries

### Selection

```
//default to limit 10
SELECT * 
FROM myTable 

SELECT * 
FROM myTable 
LIMIT 100
```

```
SELECT "date", "timestamp"
FROM myTable 
```

### Aggregation

```sql
SELECT COUNT(*), MAX(foo), SUM(bar) 
FROM myTable
```

### Grouping on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo), bar, baz 
FROM myTable
GROUP BY bar, baz 
LIMIT 50
```

### Ordering on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo), bar, baz 
FROM myTable
GROUP BY bar, baz 
ORDER BY bar, MAX(foo) DESC 
LIMIT 50
```

### Filtering

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

For performant filtering of IDs in a list, see [Filtering with IdSet](https://docs.pinot.apache.org/users/user-guide-query/filtering-with-idset).

### Filtering with NULL predicate

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE foo IS NOT NULL
  AND foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

### Selection (Projection)

```sql
SELECT * 
FROM myTable
  WHERE quux < 5
  LIMIT 50
```

### Ordering on Selection

```sql
SELECT foo, bar 
FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 100
```

### Pagination on Selection

Note that results might not be consistent if the `ORDER BY` column has the same value in multiple rows.

```sql
SELECT foo, bar 
FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 50, 100
```

### Wild-card match (in WHERE clause only)

The example below counts rows where the column `airlineName` starts with `U`:

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE REGEXP_LIKE(airlineName, '^U.*')
  GROUP BY airlineName LIMIT 10
```

### Case-When Statement

Pinot supports the `CASE-WHEN-ELSE` statement, as shown in the following two examples:

```sql
SELECT
    CASE
      WHEN price > 30 THEN 3
      WHEN price > 20 THEN 2
      WHEN price > 10 THEN 1
      ELSE 0
    END AS price_category
FROM myTable
```

```sql
SELECT
  SUM(
    CASE
      WHEN price > 30 THEN 30
      WHEN price > 20 THEN 20
      WHEN price > 10 THEN 10
      ELSE 0
    END) AS total_cost
FROM myTable
```

### UDF

Pinot doesn't currently support injecting functions.  Functions have to be implemented within Pinot, as shown below:

```sql
SELECT COUNT(*)
FROM myTable
GROUP BY DATETIMECONVERT(timeColumnName, '1:MILLISECONDS:EPOCH', '1:HOURS:EPOCH', '1:HOURS')
```

For more examples, see [Transform Function in Aggregation Grouping](https://docs.pinot.apache.org/users/user-guide-query/supported-transformations).

### BYTES column

Pinot supports queries on BYTES column using hex strings. The query response also uses hex strings to represent bytes values.

The query below fetches all the rows for a given UID:

```sql
SELECT * 
FROM myTable
WHERE UID = 'c8b3bce0b378fc5ce8067fc271a34892'
```
