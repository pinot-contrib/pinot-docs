---
description: Learn how to query Pinot using SQL
---

# Querying Pinot

## DIALECT

Pinot uses **Calcite SQL** Parser to parse queries and uses **MYSQL\_ANSI** dialect. You can see the grammar [here](https://calcite.apache.org/docs/reference.html).

## Limitations

Pinot does not support Joins or nested Subqueries and we recommend using **Presto** for queries that span multiple tables. Read [Engineering Full SQL support for Pinot at Uber](https://eng.uber.com/engineering-sql-support-on-apache-pinot/) for more info.

No DDL support. Tables can be created via the [REST API](https://docs.pinot.apache.org/users/api/pinot-rest-admin-interface).

### Identifier vs Literal

In Pinot SQL:

* **Double quotes(")** are used to force string identifiers, e.g. column name.
* **Single quotes(')** are used to enclose string literals.

Mis-using those might cause unexpected query results:

E.g.

* `WHERE a='b'` means the predicate on the column `a` equals to a string literal value `'b'`
* `WHERE a="b"` means the predicate on the column `a` equals to the value of the column `b`

## Example Queries

* Use single quotes for literals and double quotes (optional) for identifiers (column names)
* If you name the columns as `timestamp`, `date`, or other reserved keywords, or the column name includes special characters, you need to use double quotes when you refer to them in the query.

### **Simple selection**

```
//default to limit 10
SELECT * 
FROM myTable 

SELECT * 
FROM myTable 
LIMIT 100
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

### Filtering with NULL predicate

```sql
SELECT COUNT(*) 
FROM myTable
  WHERE foo IS NOT NULL
  AND foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

### Filtering with IdSet

A common use case is filtering on an id field with a list of values. This can be done with the IN clause, but this approach doesn't perform well with large lists of ids. In these cases, you can use an IdSet.

#### Create IdSet

You can create an IdSet of the values returned by a query using the _ID\_SET_ function, as shown below:

```sql
SELECT ID_SET(yearID)
FROM baseballStats
WHERE teamID = 'WS1'
```

This query returns the following:

`ATowAAABAAAAAAA7ABAAAABtB24HbwdwB3EHcgdzB3QHdQd2B3cHeAd5B3oHewd8B30Hfgd/B4AHgQeCB4MHhAeFB4YHhweIB4kHigeLB4wHjQeOB48HkAeRB5IHkweUB5UHlgeXB5gHmQeaB5sHnAedB54HnwegB6EHogejB6QHpQemB6cHqAc=`

#### Filter by values in IdSet

We can use the _IN\_ID\_SET_ function to filter a query based on an IdSet. To return rows for _yearID_s in the IdSet, check that this function returns `1` by run the following:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_ID_SET(
 yearID,   
'ATowAAABAAAAAAA7ABAAAABtB24HbwdwB3EHcgdzB3QHdQd2B3cHeAd5B3oHewd8B30Hfgd/B4AHgQeCB4MHhAeFB4YHhweIB4kHigeLB4wHjQeOB48HkAeRB5IHkweUB5UHlgeXB5gHmQeaB5sHnAedB54HnwegB6EHogejB6QHpQemB6cHqAc='
  ) = 1 
GROUP BY yearID
```

#### Filter by values not in IdSet

To return rows for _yearID_s not in the IdSet, check that the _IN\_ID\_SET_ function returns `0` by running the following:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_ID_SET(
  yearID,   
'ATowAAABAAAAAAA7ABAAAABtB24HbwdwB3EHcgdzB3QHdQd2B3cHeAd5B3oHewd8B30Hfgd/B4AHgQeCB4MHhAeFB4YHhweIB4kHigeLB4wHjQeOB48HkAeRB5IHkweUB5UHlgeXB5gHmQeaB5sHnAedB54HnwegB6EHogejB6QHpQemB6cHqAc='
  ) = 0 
GROUP BY yearID
```

### Sub Query Filtering with IdSet

The approach to using an IdSet described in the previous section requires us to send two queries, one to get the IdSet and one to filter rows based on that IdSet. We can do all this in one query using the following functions:

* IN\_SUBQUERY - Combines the two queries into one on the broker.
* IN\_PARTITIONED\_SUBQUERY - When the data is partitioned by the id column and each server contains all the data for a partition, we can directly process the subquery on the server. The generated IdSet for the first query will be smaller as it will only contain the ids for the partitions served by the server. This will give better performance.

#### Filter on broker

To filter rows for _yearID_s in the IdSet, check that _IN\_SUBQUERY_ returns `1`, by running the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 1
GROUP BY yearID  
```

To filter rows for _yearID_s not in the IdSet, check that _IN\_SUBQUERY_ returns `0`, by running the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 0
GROUP BY yearID  
```

#### Filter on server

To filter rows for _yearID_s in the IdSet, check that _IN\_PARTITIONED\_SUBQUERY_ returns `1`, by running the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_PARTITIONED_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 1
GROUP BY yearID  
```

To filter rows for _yearID_s not in the IdSet, check that _IN\_PARTITIONED\_SUBQUERY_ returns `0`, by running the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_PARTITIONED_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 0
GROUP BY yearID  
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

Note: results might not be consistent if column ordered by has same value in multiple rows.

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

As of now, functions have to be implemented within Pinot. Injecting functions is not allowed yet. The example below demonstrate the use of UDFs. More examples in [Transform Function in Aggregation Grouping](https://docs.pinot.apache.org/users/user-guide-query/supported-transformations)

```sql
SELECT COUNT(*)
FROM myTable
GROUP BY DATETIMECONVERT(timeColumnName, '1:MILLISECONDS:EPOCH', '1:HOURS:EPOCH', '1:HOURS')
```

### BYTES column

Pinot supports queries on BYTES column using HEX string. The query response also uses hex string to represent bytes value.

E.g. the query below fetches all the rows for a given UID.

```sql
SELECT * 
FROM myTable
WHERE UID = 'c8b3bce0b378fc5ce8067fc271a34892'
```
