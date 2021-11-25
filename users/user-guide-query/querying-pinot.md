---
description: Learn how to query Pinot using SQL
---

# Querying Pinot

## SQL Dialect

Pinot uses the **Calcite SQL** parser to parse queries and uses **MYSQL\_ANSI** dialect. 
You can see the grammar [in the Calcite documentation](https://calcite.apache.org/docs/reference.html).

## Limitations

Pinot does not support joins or nested subqueries.
We recommend using **Presto** for queries that span multiple tables. 
For more information, see [Engineering Full SQL support for Pinot at Uber](https://eng.uber.com/engineering-sql-support-on-apache-pinot/).

There is no DDL support. 
Tables can be created via the [REST API](https://docs.pinot.apache.org/users/api/pinot-rest-admin-interface).

## Identifier vs Literal

In Pinot SQL:

* **Double quotes(")** are used to force string identifiers, e.g. column names
* **Single quotes(')** are used to enclose string literals. If the string literal also contains a single quote, escape this with a single quote e.g  `'''Pinot'''` to match the string literal `'Pinot'`

Mis-using those might cause unexpected query results:

e.g.

* `WHERE a='b'` means the predicate on the column `a` equals to a string literal value `'b'`
* `WHERE a="b"` means the predicate on the column `a` equals to the value of the column `b`

If your column names use reserved keywords (e.g. `timestamp` or `date`) or special charactesr, you will need to use double quotes when referring to them in queries.

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

For performant filtering of ids in a list, see [Filtering with IdSet](https://docs.pinot.apache.org/users/user-guide-query/filtering-with-idset).

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


> Results might not be consistent if the order by column has the same value in multiple rows.

```sql
SELECT foo, bar 
FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 50, 100
```

### Wild-card match (in WHERE clause only)

To count rows where the column `airlineName` starts with `U`

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE REGEXP_LIKE(airlineName, '^U.*')
  GROUP BY airlineName LIMIT 10
```

### Case-When Statement

Pinot supports the CASE-WHEN-ELSE statement.

Example 1:

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

Example 2:

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

Functions have to be implemented within Pinot. Injecting functions is not yet supported. The example below demonstrate the use of UDFs. 
For more examples, see [Transform Function in Aggregation Grouping](https://docs.pinot.apache.org/users/user-guide-query/supported-transformations).

```sql
SELECT COUNT(*)
FROM myTable
GROUP BY DATETIMECONVERT(timeColumnName, '1:MILLISECONDS:EPOCH', '1:HOURS:EPOCH', '1:HOURS')
```

### BYTES column

Pinot supports queries on BYTES column using HEX string. 
The query response also uses HEX string to represent bytes values.

e.g. the query below fetches all the rows for a given UID.

```sql
SELECT * 
FROM myTable
WHERE UID = 'c8b3bce0b378fc5ce8067fc271a34892'
```
