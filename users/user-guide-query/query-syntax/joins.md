---
description: >-
  Pinot supports JOINs, including left, right, full, semi, anti, lateral, and
  equi JOINs. Use JOINs to connect two table to generate a unified view, based
  on a related column between the tables.
---

# JOINs

{% hint style="info" %}
**Important:** To query using JOINs, you must [use Pinot's multi-stage query engine (v2).](../../../reference/multi-stage-engine.md)
{% endhint %}

* [Overview of JOINs in Pinot 1.0](joins.md#joins-overview)
* [Supported JOIN types and examples](joins.md#supported-joins-types-and-examples)
* [JOIN optimizations](joins.md#joins-optimizations)

## JOINs overview

Pinot 1.0 introduces support for all JOIN types. JOINs in Pinot significantly reduce query latency and simplify architecture, achieving the best performance currently available for an OLAP database.&#x20;

Use JOINs to combine two tables (a left and right table) together, based on a related column between the tables, and other join filters. JOINs let you gain more insights from your data.

## Supported JOINs types and examples

### Inner join

The inner join selects rows that have matching values in both tables.

**Syntax:**

{% code overflow="wrap" %}
```sql
SELECT myTable.column1,myTable.column2,myOtherTable.column1,....
FROM mytable INNER JOIN table2
ON table1.matching_column = myOtherTable.matching_column;
```
{% endcode %}

#### Example of inner join

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

### Left join

A left join returns all values from the left relation and the matched values from the right table, or appends NULL if there is no match. Also referred to as a left outer join.

**Syntax:**

{% code overflow="wrap" %}
```sql
SELECT myTable.column1,table1.column2,myOtherTable.column1,....
FROM myTable LEFT JOIN myOtherTable
ON myTable.matching_column = myOtherTable.matching_column;
```
{% endcode %}

### R**ight join**

A right join returns all values from the right relation and the matched values from the left relation, or appends NULL if there is no match. It is also referred to as a right outer join.

**Syntax:**

{% code overflow="wrap" %}
```sql
SELECT table1.column1,table1.column2,table2.column1,....
FROM table1 
RIGHT JOIN table2
ON table1.matching_column = table2.matching_column;
```
{% endcode %}

### F**ull join**

A full join returns all values from both relations, appending NULL values on the side that does not have a match. It is also referred to as a full outer join.

**Syntax:**

{% code overflow="wrap" %}
```sql
SELECT table1.column1,table1.column2,table2.column1,....
FROM table1 
FULL JOIN table2
ON table1.matching_column = table2.matching_column;
```
{% endcode %}

### Cross join

A cross join returns the Cartesian product of two relations. If no WHERE clause is used along with CROSS JOIN, this produces a result set that is the number of rows in the first table multiplied by the number of rows in the second table. If a WHERE clause is included with CROSS JOIN, it functions like an [INNER JOIN](joins.md#inner-join).

**Syntax:**

```sql
SELECT * 
FROM table1 
CROSS JOIN table2;
```

### Semi/A**nti join**

Semi/anti-join returns rows from the first table where no matches are found in the second table. Returns one copy of each row in the first table for which no match is found.

**Syntax:**

```sql
SELECT  myTable.column1, myOtherTable.column1
 FROM  myOtherTable
 WHERE  NOT EXISTS [ join_criteria ]
```

### Equi join

An equi join uses an equality operator to match a single or multiple column values of the relative tables.&#x20;

**Syntax:**

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

## JOINs optimizations

Pinot JOINs include the following optimizations:

* Predicate push-down to individual tables
* Indexing and pruning to reduce scanning and speeds up query processing
* Smart data layout considerations to minimize data shuffling
* Query hints for fine-tuning JOIN operations.&#x20;





