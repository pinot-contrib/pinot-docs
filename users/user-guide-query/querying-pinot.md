---
description: Learn how to query Pinot using SQL
---

# Querying Pinot

## DIALECT

Pinot uses Calcite SQL Parser to parse queries and uses MYSQL\_ANSI dialect. You can see the grammar [here](https://calcite.apache.org/docs/reference.html). 

## Limitations

Pinot does not support Joins or nested Subqueries and we recommend using  Presto for queries that span multiple tables. Read engineering [Engineering Full SQL support for Pinot at Uber](https://eng.uber.com/engineering-sql-support-on-apache-pinot/) for more info.

No DDL support. Tables can be created via the [REST API](https://docs.pinot.apache.org/users/api/pinot-rest-admin-interface).

## Example Queries

* Use single quotes for literals and double quotes \(optional\) for identifiers \(column names\)
* If you name your columns as timestamp, date, and other reserved keywords, you need to use double quotes when you refer to them in the query.

  
**Simple selection**

```
//default to limit 10
SELECT * FROM myTable 

SELECT * FROM myTable LIMIT 100
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

### Filtering with NULL predicate

```sql
SELECT COUNT(*) FROM myTable
  WHERE foo IS NOT NULL
  AND foo = 'foo'
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
FROM SomeTable
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
FROM
    SomeTable
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



