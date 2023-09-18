---
description: >-
  Pinot supports JOINs, including left, right, full, semi, anti, lateral, and
  equi JOINs. Use JOINs to stitch two table to generate a unified view, based on
  a related column between the tables.
---

# JOINs

{% hint style="info" %}
**Important:** To query using JOINs, you must [use Pinot's multi-stage query engine (v2).](../../developers/advanced/v2-multi-stage-query-engine.md)
{% endhint %}

Use JOINs to stitch two tables (a left and right table) together to generate a unified view, based on a related column between the tables. JOINs let you gain more insights from your data.

Pinot supports the following JOINs:

* Left
* Right
* Full
* Semi
* Anti
* Lateral&#x20;
* Equi



## Window function query syntax

The standard SQL query syntax for window function is:

```
function(args) OVER (
    [PARTITION BY expression]
    [ORDER BY expression [ASC|DESC]]
    [frame]
)
```

### Example query layout

The following query shows the complete components of window function.&#x20;

{% code overflow="wrap" %}
```
SELECT FUNC(column1) OVER ([PARTITION BY column2] [ORDER BY column3] [ROWS 2 PRECEDING])
    FROM tableName
    WHERE filter_clause  
```
{% endcode %}

## OVER clause

The OVER clause applies a specified[ supported Windows function](joins.md#supported-pinot-window-functions) to compute values over a group of rows, and return a single result for each row. The OVER clause specifies how the rows are arranged and how the aggregation is done on those rows.

Inside the over clause, there are three optional components, i.e. PARTITION BY clause, ORDER BY clause, and FRAME clause.

#### Partition by Clause

PARTITION BY clause is firstly done among all three components.

If a PARTITION BY clause is specified, the intermediate results will be grouped into different partitions based on the values of the columns appearing in the PARTITION BY clause.

If the PARTITION BY clause isn’t specified, the whole result will be regarded as one big partition, i.e. there is only one partition in the result set.

#### Order by Clause

ORDER BY clause is done after partitioning is done in the window function.

If an ORDER BY clause is specified, all the rows within the same partition will be sorted based on the values of the columns appearing in the window ORDER BY clause. The ORDER BY clause decides the order in which the rows within a partition are to be processed.

If no ORDER BY clause is specified while a PARTITION BY clause is specified, the order of the rows is undefined. If output ordering is desired a global ORDER BY clause should be used in the query.

#### Frame Clause

FRAME clause is to define the boundary of the frame for every row in the result set. This is usually done along with the aggregate function in the window function.

A FRAME is one of:

{RANGE|ROWS} frame\_start

{RANGE|ROWS} BETWEEN frame\_start AND frame\_end; frame\_start and frame\_end can be any of:

UNBOUNDED PRECEDING

expression PRECEDING  -- maybe only allowed in ROWS mode \[depends on DB, some support some don’t]

CURRENT ROW

expression FOLLOWING  -- maybe only allowed in ROWS mode \[depends on DB, some support some don’t]

UNBOUNDED FOLLOWING

If no FRAME clause is specified, then the default frame behavior depends on whether ORDER BY is present or not. If only a PARTITION BY clause is present then the default frame behavior is to calculate the aggregation from UNBOUNDED PRECEDING to UNBOUNDED FOLLOWING. If an ORDER BY clause is specified, the default behavior is to calculate the aggregation from the beginning of the partition to the current row or UNBOUNDED PRECEDING to CURRENT ROW.

If there is no FRAME, no PARTITION BY, and no ORDER BY clause specified in the OVER clause (empty OVER), the whole result set will be regarded as one partition, and there is only one big frame inside the window.

## Supported Pinot window functions



| Function                                                                                                    | Description                                                                                                                         | Example            | Default Value When No Record Selected |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------- |
| [**AVG**](https://github.com/pinot-contrib/pinot-docs/blob/master/configuration-reference/functions/avg.md) | Returns the average of the values for a numeric column as a`Double over the specified number of rows or partition (if applicable).` | `AVG(playerScore)` | `Double.NEGATIVE_INFINITY`            |
| BOOL\_AND                                                                                                   | Returns true if all input values are true, otherwise false                                                                          |                    |                                       |
| BOOL\_OR                                                                                                    | Returns true if at least one input value is true, otherwise false                                                                   |                    |                                       |
| [**COUNT**](../../configuration-reference/functions/count.md)                                               | Returns the count of the records as `Long`                                                                                          | `COUNT(*)`         | `0`                                   |
| [**MIN**](../../configuration-reference/functions/min.md)                                                   | Returns the minimum value of a numeric column as `Double`                                                                           | `MIN(playerScore)` | `Double.POSITIVE_INFINITY`            |
| [**MAX**](../../configuration-reference/functions/max.md)                                                   | Returns the maximum value of a numeric column as `Double`                                                                           | `MAX(playerScore)` | `Double.NEGATIVE_INFINITY`            |
| ROW\_NUMBER                                                                                                 |                                                                                                                                     |                    |                                       |
| [**SUM**](../../configuration-reference/functions/sum.md)                                                   | Returns the sum of the values for a numeric column as `Double`                                                                      | `SUM(playerScore)` | `0`                                   |

## Examples of windows functions

* [Sum transactions by customer ID](joins.md#sum-transactions-by-customer-id)
* [Find the maximum transaction by customer ID](joins.md#find-the-maximum-transaction-by-customer-id)
* [Find the minimum transaction by customer ID](joins.md#find-the-minimum-transaction-by-customer-id)
* [Find the average transaction amount by customer ID](joins.md#find-the-average-transaction-amount-by-customer-id)

### Sum transactions by customer ID

Calculate the rolling sum transaction amount ordered by the payment date for each customer ID (note, the default frame here is UNBOUNDED PRECEDING and CURRENT ROW).

{% code overflow="wrap" %}
```
SELECT customer_id, payment_date, amount, SUM(amount) OVER(PARTITION BY customer_id ORDER BY payment_date) from payment;
```
{% endcode %}

|  customer\_id  |   payment\_date             | amount |  sum   |
| -------------- | --------------------------- | ------ | ------ |
| 1              | 2023-02-14 23:22:38.996577  | 5.99   | 5.99   |
| 1              |  2023-02-15 16:31:19.996577 | 0.99   |  6.98  |
| 1              | 2023-02-15 19:37:12.996577  | 9.99   |  16.97 |
| 1              | 2023-02-16 13:47:23.996577  | 4.99   |  21.96 |
|                |                             |        |        |
|                |                             |        |        |

&#x20;customer\_id |        payment\_date        | amount |  sum  &#x20;

\-------------+----------------------------+--------+--------

&#x20;          2 | 2007-02-17 19:23:24.996577 |   2.99 |   2.99

&#x20;          2 | 2007-03-01 08:13:52.996577 |   0.99 |   3.98

&#x20;          3 | 2007-02-16 00:02:31.996577 |   8.99 |   8.99

&#x20;          3 | 2007-02-16 13:47:36.996577 |   6.99 |  15.98

&#x20;          3 | 2007-02-17 03:43:41.996577 |   6.99 |  22.97

&#x20;          3 | 2007-02-19 07:03:19.996577 |   2.99 |  25.96

&#x20;          3 | 2007-03-01 12:48:14.996577 |   5.99 |  31.95

&#x20;          4 | 2007-02-15 07:59:54.996577 |   4.99 |   4.99

&#x20;          4 | 2007-02-16 06:37:06.996577 |   0.99 |   5.98

&#x20;          4 | 2007-02-16 12:29:53.996577 |   2.99 |   8.97\


### Find the maximum transaction by customer ID

Calculate the least expensive transaction made by each customer comparing all transactions made by the customer (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

{% code overflow="wrap" %}
```
SELECT customer_id, payment_date, amount, MIN(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

&#x20;customer\_id |        payment\_date        | amount |  min &#x20;

\-------------+----------------------------+--------+-------

&#x20;          1 | 2007-02-14 23:22:38.996577 |   5.99 |  0.99

&#x20;          1 | 2007-02-15 16:31:19.996577 |   0.99 |  0.99

&#x20;          1 | 2007-02-15 19:37:12.996577 |   9.99 |  0.99

&#x20;          1 | 2007-02-16 13:47:23.996577 |   4.99 |  0.99

&#x20;          2 | 2007-04-30 04:34:36.996577 |   4.99 |  4.99

&#x20;          2 | 2007-04-30 12:16:09.996577 |  10.99 |  4.99

&#x20;          3 | 2007-03-23 05:38:40.996577 |   2.99 |  2.99

&#x20;          3 | 2007-04-07 08:51:51.996577 |   4.99 |  2.99

&#x20;          3 | 2007-04-08 11:15:37.996577 |   4.99 |  2.99

&#x20;          3 | 2007-04-27 03:23:08.996577 |   5.99 |  2.99

&#x20;          3 | 2007-04-27 18:51:38.996577 |  10.99 |  2.99

&#x20;          3 | 2007-04-28 02:27:47.996577 |   7.99 |  2.99

&#x20;          4 | 2007-03-18 03:43:10.996577 |   8.99 |  1.99

&#x20;          4 | 2007-03-19 00:47:39.996577 |   1.99 |  1.99

&#x20;          4 | 2007-03-20 08:00:30.996577 |   2.99 |  1.99\


### Find the minimum transaction by customer ID

Calculate the least expensive transaction made by each customer compared all transactions made by the customer (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

{% code overflow="wrap" %}
```
SELECT customer_id, payment_date, amount, MIN(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

&#x20;customer\_id |        payment\_date        | amount |  min &#x20;

\-------------+----------------------------+--------+-------

&#x20;          1 | 2007-02-14 23:22:38.996577 |   5.99 |  0.99

&#x20;          1 | 2007-02-15 16:31:19.996577 |   0.99 |  0.99

&#x20;          1 | 2007-02-15 19:37:12.996577 |   9.99 |  0.99

&#x20;          1 | 2007-02-16 13:47:23.996577 |   4.99 |  0.99

&#x20;          2 | 2007-04-30 04:34:36.996577 |   4.99 |  4.99

&#x20;          2 | 2007-04-30 12:16:09.996577 |  10.99 |  4.99

&#x20;          3 | 2007-03-23 05:38:40.996577 |   2.99 |  2.99

&#x20;          3 | 2007-04-07 08:51:51.996577 |   4.99 |  2.99

&#x20;          3 | 2007-04-08 11:15:37.996577 |   4.99 |  2.99

&#x20;          3 | 2007-04-27 03:23:08.996577 |   5.99 |  2.99

&#x20;          3 | 2007-04-27 18:51:38.996577 |  10.99 |  2.99

&#x20;          3 | 2007-04-28 02:27:47.996577 |   7.99 |  2.99

&#x20;          4 | 2007-03-18 03:43:10.996577 |   8.99 |  1.99

&#x20;          4 | 2007-03-19 00:47:39.996577 |   1.99 |  1.99

&#x20;          4 | 2007-03-20 08:00:30.996577 |   2.99 |  1.99

### Find the average transaction amount by customer ID

Calculate a customer’s average transaction amount for all transactions they’ve made (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

{% code overflow="wrap" %}
```
SELECT customer_id, payment_date, amount, AVG(amount) OVER(PARTITION BY customer_id) from payment;

```
{% endcode %}





