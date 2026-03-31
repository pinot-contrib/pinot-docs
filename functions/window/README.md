---
description: >-
  Use window functions to compute averages, sort, rank, or count items,
  calculate sums, and find minimum or maximum values across windows.
---

# Window Functions



{% hint style="info" %}
**Important:** To query using Windows functions, you must enable Pinot's [multi-stage query engine (v2)](../../configuration-reference/cluster.md). See how to [enable and use the multi-stage query engine (v2](../../build-with-pinot/querying-and-sql/sse-vs-mse.md)).
{% endhint %}

## Window Functions overview

This is an overview of the window functions feature.

### Window function syntax

Pinot's window function (`windowedCall`) has the following syntax definition:

{% code overflow="wrap" %}
```sql
windowedCall:
      windowFunction
      OVER 
      window

windowFunction:
      function_name '(' value [, value ]* ')'
   |
      function_name '(' '*' ')'

window:
      '('
      [ PARTITION BY expression [, expression ]* ]
      [ ORDER BY orderItem [, orderItem ]* ]
      [
          RANGE BETWEEN frame_start AND frame_end
        |   
          ROWS BETWEEN frame_start AND frame_end
        |
          RANGE frame_start
        |
          ROWS frame_start    
      ]
      ')'
      
frame_start:
      UNBOUNDED PRECEDING
    |
      offset PRECEDING
    |
      CURRENT ROW
    |  
      offset FOLLOWING
     
frame_end:
      offset PRECEDING
    |
      CURRENT ROW
    |
      offset FOLLOWING
    |
      UNBOUNDED FOLLOWING       
```
{% endcode %}

* `windowedCall` refers to the actual windowed operation.
* `windowFunction` refers to the window function used, see supported [window functions](#window-functions).
* `window` is the window definition / windowing mechanism, see supported [window mechanism](#window-mechanism-over-clause).

You can jump to the [examples](#examples-of-windows-functions) section to see more concrete use cases of window functions in Pinot.

### Example window function query layout

The following query shows the complete components of the window function. Note that the `PARTITION BY` ,`ORDER BY`, and the `FRAME` clauses are all optional.

{% code overflow="wrap" %}
```sql
SELECT FUNC(column1) OVER (PARTITION BY column2 ORDER BY column3 RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
    FROM tableName
    WHERE filter_clause  
```
{% endcode %}

## Window mechanism (OVER clause)

#### Partition by clause

* If a `PARTITION BY` clause is specified, the intermediate results will be grouped into different partitions based on the values of the columns appearing in the `PARTITION BY` clause.
* If the `PARTITION BY` clause isn’t specified, the whole result will be regarded as one big partition, i.e. there is only one partition in the result set.

#### Order by clause

* If an `ORDER BY` clause is specified, all the rows within the same partition will be sorted based on the values of the columns appearing in the window `ORDER BY` clause. The `ORDER BY` clause decides the order in which the rows within a partition are to be processed.&#x20;
* If no `ORDER BY` clause is specified while a `PARTITION BY` clause is specified, the order of the rows is undefined. To order the output, use a global `ORDER BY` clause in the query.

#### Frame clause

{% hint style="warning" %}
`RANGE` type window frames currently cannot be used with `offset PRECEDING` / `offset FOLLOWING`
{% endhint %}

The following window frame clauses are currently supported:

* `RANGE frame_start` where `frame_start` can be `UNBOUNDED PRECEDING` or `CURRENT ROW` (`frame_end` will default to `CURRENT ROW`)
* `ROWS frame_start` where `frame_start` can be `UNBOUNDED PRECEDING`, `offset PRECEDING`,  or `CURRENT ROW` (`frame_end` will default to `CURRENT ROW`)
* `RANGE BETWEEN frame_start AND frame_end`; `frame_start` can be either `UNBOUNDED PRECEDING` or `CURRENT ROW` and `frame_end` can be either `CURRENT ROW` or `UNBOUNDED FOLLOWING`
* `ROWS BETWEEN frame_start AND frame_end`; `frame_start` / `frame_end` can be one of:
  * `UNBOUNDED PRECEDING` (`frame_start` only)
  * `offset PRECEDING` where `offset` is an integer literal
  * `CURRENT ROW`
  * `offset FOLLOWING` where `offset` is an integer literal
  * `UNBOUNDED FOLLOWING` (`frame_end` only)

In `RANGE` mode, a `frame_start` of `CURRENT ROW` means the frame starts with the current row's first _peer_ row (a row that the window's `ORDER BY` clause sorts as equivalent to the current row), while a `frame_end` of `CURRENT ROW` means the frame ends with the current row's last peer row. In `ROWS` mode, `CURRENT ROW` simply means the current row.

If no `ORDER BY` clause is specified, the window frame will always be `RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` and cannot be modified. When an `ORDER BY` clause is present, the default frame is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` if no explicit window frame is defined in the query.&#x20;

If there is no `FRAME`, no `PARTITION BY`, and no `ORDER BY` clause specified in the OVER clause (empty `OVER`), the whole result set is regarded as one partition, and there's one frame in the window.

The `OVER` clause applies a specified supported [windows function](#window-aggregate-functions) to compute values over a group of rows and return a single result for each row. The `OVER` clause specifies how the rows are arranged and how the aggregation is done on those rows.

Inside the over clause, there are three optional components: `PARTITION BY` clause, `ORDER BY` clause, and `FRAME` clause.

## Window functions

Window functions are commonly used to do the following:

* [Compute averages](#find-the-average-transaction-amount-by-customer-id)
* [Rank items](#rank-year-to-date-sales-for-a-sales-team)
* [Count items](#count-the-number-of-transactions-by-customer-id)
* [Calculate sums](#sum-transactions-by-customer-id)
* [Find minimum or maximum values](#find-the-minimum-or-maximum-transaction-by-customer-id)

Supported window functions are listed in the following table.

<table><thead><tr><th>Function</th><th>Description</th><th width="198">Example</th><th>Default Value When No Record Selected</th></tr></thead><tbody><tr><td><a href="../../functions/aggregation/avgmv.md"><strong>AVG</strong></a></td><td>Returns the average of the values for a numeric column in the defined window.</td><td><code>AVG(playerScore)</code></td><td><code>Double.NEGATIVE_INFINITY</code></td></tr><tr><td>BOOL_AND</td><td>Returns <code>false</code> if even a single value in the window is <code>false</code>, <code>null</code> if a single value in the window is <code>null</code>, and <code>true</code> if all the values in the window are <code>true</code>.</td><td></td><td><code>null</code></td></tr><tr><td>BOOL_OR</td><td>Returns <code>true</code> if even a single value in the window is <code>true</code> , <code>null</code> if a single value in the window is <code>null</code>, and <code>false</code> if all the values in the window are <code>false</code>.</td><td></td><td><code>null</code></td></tr><tr><td><a href="../../functions/aggregation/count.md"><strong>COUNT</strong></a></td><td>Returns the number of values in the window</td><td><code>COUNT(*)</code></td><td><code>0</code></td></tr><tr><td><a href="../../functions/aggregation/min.md"><strong>MIN</strong></a></td><td>Returns the minimum value of a numeric column as <code>Double</code></td><td><code>MIN(playerScore)</code></td><td><code>null</code></td></tr><tr><td><a href="../../functions/aggregation/max.md"><strong>MAX</strong></a></td><td>Returns the maximum value of a numeric column as <code>Double</code></td><td><code>MAX(playerScore)</code></td><td><code>null</code></td></tr><tr><td><a href="../../functions/aggregation/sum.md"><strong>SUM</strong></a></td><td>Returns the sum of the values for a numeric column as <code>Double</code></td><td><code>SUM(playerScore)</code></td><td><code>null</code></td></tr><tr><td><a href="../../functions/aggregation/lead.md">LEAD</a></td><td>The <code>LEAD</code> function provides access to a subsequent row within the same result set, without the need for a self-join.</td><td><code>LEAD(column_name, offset, default_value)</code></td><td></td></tr><tr><td><a href="../../functions/aggregation/lag.md">LAG</a></td><td>The <code>LAG</code> function provides access to a previous row within the same result set, without the need for a self-join.</td><td><code>LAG(column_name, offset, default_value)</code></td><td></td></tr><tr><td><a href="../../functions/aggregation/first_value.md">FIRST_VALUE</a></td><td>The <code>FIRST_VALUE</code> function returns the value from the first row in the window.</td><td><code>FIRST_VALUE(salary)</code></td><td></td></tr><tr><td><a href="../../functions/aggregation/last_value.md">LAST_VALUE</a></td><td>The <code>LAST_VALUE</code> function returns the value from the last row in the window</td><td><code>LAST_VALUE(salary)</code></td><td></td></tr><tr><td><a href="../../functions/math/round-1-1.md">ROW_NUMBER</a></td><td>Returns the number of the current row within its partition, counting from 1.</td><td><code>ROW_NUMBER()</code></td><td></td></tr><tr><td>RANK</td><td>Returns the rank of the current row, with gaps - i.e., the <code>row_number</code> of the first row in its peer group.</td><td><code>RANK()</code></td><td></td></tr><tr><td>DENSE_RANK</td><td>Returns the rank of the current row, without gaps.</td><td><code>DENSE_RANK()</code></td><td></td></tr></tbody></table>

Note that no window frame clause can be specified for `ROW_NUMBER`, `RANK`, and `DENSE_RANK` window functions since they're applied on the entire partition by definition. Similarly, no window frame clause can be specified for `LAG` and `LEAD` since the row `offset` is an input to those functions themselves.

## Window aggregate query examples

* [Sum transactions by customer ID](#sum-transactions-by-customer-id)
* [Find the minimum or maximum transaction by customer ID](#find-the-minimum-or-maximum-transaction-by-customer-id)
* [Find the average transaction amount by customer ID](#find-the-average-transaction-amount-by-customer-id)
* [Rank year-to-date sales for a sales team](#rank-year-to-date-sales-for-a-sales-team)
* [Count the number of transactions by customer ID](#count-the-number-of-transactions-by-customer-id)

### Sum transactions by customer ID

Calculate the rolling sum transaction amount ordered by the payment date for each customer ID (note, the default frame here is `UNBOUNDED PRECEDING` and `CURRENT ROW`).

{% code overflow="wrap" %}
```
SELECT customer_id, payment_date, amount, SUM(amount) OVER(PARTITION BY customer_id ORDER BY payment_date) from payment;
```
{% endcode %}

| customer\_id | payment\_date              | amount | sum   |
| ------------ | -------------------------- | ------ | ----- |
| 1            | 2023-02-14 23:22:38.996577 | 5.99   | 5.99  |
| 1            | 2023-02-15 16:31:19.996577 | 0.99   | 6.98  |
| 1            | 2023-02-15 19:37:12.996577 | 9.99   | 16.97 |
| 1            | 2023-02-16 13:47:23.996577 | 4.99   | 21.96 |
| 2            | 2023-02-17 19:23:24.996577 | 2.99   | 2.99  |
| 2            | 2023-02-17 19:23:24.996577 | 0.99   | 3.98  |
| 3            | 2023-02-16 00:02:31.996577 | 8.99   | 8.99  |
| 3            | 2023-02-16 13:47:36.996577 | 6.99   | 15.98 |
| 3            | 2023-02-17 03:43:41.996577 | 6.99   | 22.97 |
| 4            | 2023-02-15 07:59:54.996577 | 4.99   | 4.99  |
| 4            | 2023-02-16 06:37:06.996577 | 0.99   | 5.98  |

### Find the minimum or maximum transaction by customer ID

Calculate the least (use `MIN()`) or most expensive (use `MAX()`) transaction made by each customer comparing all transactions made by the customer (default frame here is `UNBOUNDED PRECEDING` and `UNBOUNDED FOLLOWING`). The following query shows how to find the least expensive transaction.

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, MIN(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

<table><thead><tr><th>customer_id</th><th width="224">payment_date</th><th width="160">amount</th><th data-type="number">min</th></tr></thead><tbody><tr><td>1</td><td>2023-02-14 23:22:38.996577</td><td>5.99</td><td>0.99</td></tr><tr><td>1</td><td>2023-02-15 16:31:19.996577</td><td>0.99</td><td>0.99</td></tr><tr><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td><td>0.99</td></tr><tr><td>2</td><td>2023-04-30 04:34:36.996577</td><td>4.99</td><td>4.99</td></tr><tr><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td><td>4.99</td></tr><tr><td>3</td><td>2023-03-23 05:38:40.996577</td><td>2.99</td><td>2.99</td></tr><tr><td>3</td><td>2023-04-07 08:51:51.996577</td><td>3.99</td><td>2.99</td></tr><tr><td>3</td><td>3 | 2023-04-08 11:15:37.996577</td><td>4.99</td><td>2.99</td></tr></tbody></table>

### Find the average transaction amount by customer ID

Calculate a customer’s average transaction amount for all transactions they’ve made (default frame here is `UNBOUNDED PRECEDING` and `UNBOUNDED FOLLOWING`).

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, AVG(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

<table><thead><tr><th>customer_id</th><th>payment_date</th><th width="131">amount</th><th data-type="number">avg</th></tr></thead><tbody><tr><td>1</td><td>2023-02-14 23:22:38.996577</td><td>5.99</td><td>5.66</td></tr><tr><td>1</td><td>2023-02-15 16:31:19.996577</td><td>0.99</td><td>5.66</td></tr><tr><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td><td>5.66</td></tr><tr><td>2</td><td>2023-04-30 04:34:36.996577</td><td>4.99</td><td>7.99</td></tr><tr><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td><td>7.99</td></tr><tr><td>3</td><td>2023-03-23 05:38:40.996577</td><td>2.99</td><td>3.99</td></tr><tr><td>3</td><td>2023-04-07 08:51:51.996577</td><td>3.99</td><td>3.99</td></tr><tr><td>3</td><td>2023-04-08 11:15:37.996577</td><td>4.99</td><td>3.99</td></tr></tbody></table>

### Rank year-to-date sales for a sales team

Use `ROW_NUMBER()` to rank team members by their year-to-date sales (default frame here is `UNBOUNDED PRECEDING` and `UNBOUNDED FOLLOWING`).

{% code overflow="wrap" %}
```sql
SELECT ROW_NUMBER() OVER(ORDER BY SalesYTD DESC) AS Row,   
    FirstName, LastName AS "Total sales YTD"   
FROM Sales.vSalesPerson;  
```
{% endcode %}

<table><thead><tr><th>Row</th><th width="257">FirstName</th><th width="122">LastName</th><th data-type="number">Total sales YTD</th></tr></thead><tbody><tr><td>1</td><td>Joe</td><td>Smith</td><td>2251368.34</td></tr><tr><td>2</td><td>Alice</td><td>Davis</td><td>2151341.64</td></tr><tr><td>3</td><td>James</td><td>Jones</td><td>1551363.54</td></tr><tr><td>4</td><td>Dane</td><td>Scott</td><td>1251358.72</td></tr></tbody></table>

### Count the number of transactions by customer ID

Count the number of transactions made by each customer (default frame here is `UNBOUNDED PRECEDING` and `UNBOUNDED FOLLOWING`).

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, count(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

| customer\_id | payment\_date              | amount | count |
| ------------ | -------------------------- | ------ | ----- |
| 1            | 2023-02-14 23:22:38.99657  | 10.99  | 2     |
| 1            | 2023-02-15 16:31:19.996577 | 8.99   | 2     |
| 2            | 2023-04-30 04:34:36.996577 | 23.50  | 3     |
| 2            | 2023-04-07 08:51:51.996577 | 12.35  | 3     |
| 2            | 2023-04-08 11:15:37.996577 | 8.29   | 3     |
