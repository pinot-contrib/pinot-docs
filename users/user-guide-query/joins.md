---
description: >-
  Pinot supports JOINs, including left, right, full, semi, anti, lateral, and
  equi JOINs. Use JOINs to connect two table to generate a unified view, based
  on a related column between the tables.
---

# JOINs

This page explains the syntax used to write join. In order to get a more in deep knowledge of how joins work it is recommended to read [Optimizing joins](multi-stage-query/optimizing-joins.md) and also [this blog](https://startree.ai/resources/query-time-joins-in-apache-pinot-1-0) from Star Tree.

{% hint style="info" %}
**Important:** To query using JOINs, you must [use Pinot's multi-stage query engine (v2).](../../reference/multi-stage-engine.md)
{% endhint %}

## INNER JOIN

The inner join selects rows that have matching values in both tables.

### **Syntax**

{% code overflow="wrap" %}
```sql
SELECT myTable.column1,myTable.column2,myOtherTable.column1,....
FROM mytable INNER JOIN table2
ON table1.matching_column = myOtherTable.matching_column;
```
{% endcode %}

### Example of inner join

Joins a table containing user transactions with a table containing promotions shown to the users, to show the spending for every userID.

{% code overflow="wrap" %}
```sql
SELECT 
  p.userID, t.spending_val

FROM promotion AS p JOIN transaction AS t 
  ON p.userID = t.userID

WHERE
  p.promotion_val > 10
  AND t.transaction_type IN ('CASH', 'CREDIT')  
  AND t.transaction_epoch >= p.promotion_start_epoch
  AND t.transaction_epoch < p.promotion_end_epoch  
```
{% endcode %}

## LEFT JOIN

A left join returns all values from the left relation and the matched values from the right table, or appends NULL if there is no match. Also referred to as a left outer join.

### **Syntax:**

{% code overflow="wrap" %}
```sql
SELECT myTable.column1,table1.column2,myOtherTable.column1,....
FROM myTable LEFT JOIN myOtherTable
ON myTable.matching_column = myOtherTable.matching_column;
```
{% endcode %}

## RIGHT JOIN

A right join returns all values from the right relation and the matched values from the left relation, or appends NULL if there is no match. It is also referred to as a right outer join.

### Syntax:

{% code overflow="wrap" %}
```sql
SELECT table1.column1,table1.column2,table2.column1,....
FROM table1 
RIGHT JOIN table2
ON table1.matching_column = table2.matching_column;
```
{% endcode %}

## FULL JOIN

A full join returns all values from both relations, appending NULL values on the side that does not have a match. It is also referred to as a full outer join.

### **Syntax:**

{% code overflow="wrap" %}
```sql
SELECT table1.column1,table1.column2,table2.column1,....
FROM table1 
FULL JOIN table2
ON table1.matching_column = table2.matching_column;
```
{% endcode %}

## CROSS JOIN

A cross join returns the Cartesian product of two relations. If no WHERE clause is used along with CROSS JOIN, this produces a result set that is the number of rows in the first table multiplied by the number of rows in the second table. If a WHERE clause is included with CROSS JOIN, it functions like an [INNER JOIN](joins.md#inner-join).

### **Syntax:**

```sql
SELECT * 
FROM table1 
CROSS JOIN table2;
```

## SEMI JOIN

Semi-join returns rows from the first table where matches are found in the second table. Returns one copy of each row in the first table for which a match is found.

### **Syntax:**

```sql
SELECT myTable.column1, myOtherTable.column1
 FROM myOtherTable
 WHERE EXISTS [ join_criteria ]
```

Some subqueries, like the following are also implemented as a semi-join under the hood:

```sql
SELECT table1.strCol
 FROM  table1
 WHERE table1.intCol IN (select table2.anotherIntCol from table2 where ...)
```

## ANTI JOIN

Anti-join returns rows from the first table where no matches are found in the second table. Returns one copy of each row in the first table for which no match is found.

### **Syntax:**

```sql
SELECT myTable.column1, myOtherTable.column1
 FROM myOtherTable
 WHERE NOT EXISTS [ join_criteria ]
```

Some subqueries, like the following are also implemented as an anti-join under the hood:

```sql
SELECT table1.strCol
 FROM  table1
 WHERE table1.intCol NOT IN (select table2.anotherIntCol from table2 where ...)
```

## Equi join

An equi join uses an equality operator to match a single or multiple column values of the relative tables.&#x20;

### **Syntax:**

```sql
SELECT *
FROM table1 
JOIN table2
[ON (join_condition)]

OR

SELECT column_list 
FROM table1, table2....
WHERE table1.column_name =
table2.column_name; 
```

## ASOF JOIN

An `ASOF JOIN` selects rows from two tables based on a "closest match" algorithm.&#x20;

### Syntax:

```sql
SELECT * FROM table1 ASOF JOIN table2 
MATCH_CONDITION(table1.col1 <comparison_operator> table2.col1))
ON table1.col2 = table2.col2;
```

The comparison operator in the `MATCH_CONDITION` can be one out of - `<`, `>`, `<=`, `>=`. Similar to an inner join, an ASOF join first calculate the set of matching rows in the right table for each row in the left table based on the `ON` condition. But instead of returning all of these rows, the only one returned is the closest match (if one exists) based on the match condition. Note that the two columns in the `MATCH_CONDITION` should be of the same type.

The join condition in `ON` is mandatory and has to be a conjunction of equality comparisons (i.e., non-equi join conditions and clauses joined with `OR` aren't allowed). `ON true` can be used in case the join should only be performed using the `MATCH_CONDITION`.

## LEFT ASOF JOIN

A `LEFT ASOF JOIN` is similar to the `ASOF JOIN`, with the only difference being that all rows from the left table are returned, even those without a match in the right table with the unmatched rows being padded with `NULL` values (similar to the difference between an `INNER JOIN` and a `LEFT JOIN`).

### Syntax:

```sql
SELECT * FROM table1 LEFT ASOF JOIN table2 
MATCH_CONDITION(table1.col1 <comparison_operator> table2.col1))
ON table1.col2 = table2.col2;
```
