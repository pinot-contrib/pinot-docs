---
description: >-
  Use window aggregate to compute averages, sort, rank, or count items,
  calculate sums, and find minimum or maximum values across window.
---

# Window aggregate

{% hint style="info" %}
**Important:** To query using Windows functions, you must enable Pinot's [multi-stage query engine (v2)](https://docs.pinot.apache.org/reference/cluster-1). See how to [enable and use the multi-stage query engine (v2](https://docs.pinot.apache.org/developers/advanced/v2-multi-stage-query-engine)).
{% endhint %}

## Window aggregate overview

This is an overview of the window aggregate feature.

### Window aggregate syntax

Pinot's window function (`windowedAggCall`) includes the following syntax definition:

{% code overflow="wrap" %}
```sql
windowedAggCall:
      windowAggFunction
      OVER 
      window

windowAggFunction:
      agg '(' [ ALL | DISTINCT ] value [, value ]* ')'
   |
      agg '(' '*' ')'

window:
      '('
      [ PARTITION BY expression [, expression ]* ]
      [ ORDER BY orderItem [, orderItem ]* ]
      [
          RANGE numericOrIntervalExpression { PRECEDING | FOLLOWING }
      |   ROWS numericExpression { PRECEDING | FOLLOWING }
      ]
      ')'
```
{% endcode %}

* `windowAggCall` refers to the actual windowed agg operation.
* `windowAggFunction` refers to the aggregation function used inside a windowed aggregate, see supported [window aggregate functions](windows-functions.md).
* `window` is the window definition / windowing mechanism, see supported [window mechanism](windows-functions.md#window-mechanism-over-clause).

You can jump to the [examples](windows-functions.md#examples-of-windows-functions) section to see more concrete use cases of window aggregate on Pinot.

### Example window aggregate query layout

The following query shows the complete components of the window function. Note, `PARTITION BY` and `ORDER BY` are optional.

{% code overflow="wrap" %}
```sql
SELECT FUNC(column1) OVER (PARTITION BY column2 ORDER BY column3)
    FROM tableName
    WHERE filter_clause  
```
{% endcode %}

## Window mechanism (OVER clause)

#### Partition by clause

* If a PARTITION BY clause is specified, the intermediate results will be grouped into different partitions based on the values of the columns appearing in the PARTITION BY clause.
* If the PARTITION BY clause isn’t specified, the whole result will be regarded as one big partition, i.e. there is only one partition in the result set.

#### Order by clause

* If an ORDER BY clause is specified, all the rows within the same partition will be sorted based on the values of the columns appearing in the window `ORDER BY` clause. The ORDER BY clause decides the order in which the rows within a partition are to be processed.
* If no ORDER BY clause is specified while a PARTITION BY clause is specified, the order of the rows is undefined. To order the output, use a global `ORDER BY` clause in the query.

#### Frame clause

{% hint style="warning" %}
**Important Note**: in release 1.0.0 window aggregate only supports `UNBOUND PRECEDING`, `UNBOUND FOLLOWING` and `CURRENT ROW`. frame and row count support have not been implemented yet.
{% endhint %}

* {RANGE|ROWS} frame\_start OR
* {RANGE|ROWS} BETWEEN frame\_start AND frame\_end; frame\_start and frame\_end can be any of:
  * UNBOUNDED PRECEDING: expression PRECEDING. May only be allowed in ROWS mode \[depends on DB, some support some don’t]
  * CURRENT ROW expression FOLLOWING. May only be allowed in ROWS mode \[depends on DB, some support some don’t]
  * UNBOUNDED FOLLOWING:
    * If no FRAME clause is specified, then the default frame behavior depends on whether ORDER BY is present or not.
    * If an ORDER BY clause is specified, the default behavior is to calculate the aggregation from the beginning of the partition to the current row or UNBOUNDED PRECEDING to CURRENT ROW.
    * If only a PARTITION BY clause is present, the default frame behavior is to calculate the aggregation from UNBOUNDED PRECEDING to CURRENT ROW.

If there is no FRAME, no PARTITION BY, and no ORDER BY clause specified in the OVER clause (empty OVER), the whole result set is regarded as one partition, and there's one frame in the window.

The OVER clause applies a specified supported [windows aggregate function](windows-functions.md#window-aggregate-functions) to compute values over a group of rows and return a single result for each row. The OVER clause specifies how the rows are arranged and how the aggregation is done on those rows.

Inside the over clause, there are three optional components: PARTITION BY clause, ORDER BY clause, and FRAME clause.

## Window aggregate functions

Window aggregate functions are commonly used to do the following:

* [Compute averages](windows-functions.md#find-the-average-transaction-amount-by-customer-id)
* [Rank items](windows-functions.md#rank-year-to-date-sales-for-a-sales-team)
* [Count items](windows-functions.md#count-the-number-of-transactions-by-customer-id)
* [Calculate sums](windows-functions.md#sum-transactions-by-customer-id)
* [Find minimum or maximum values](windows-functions.md#find-the-minimum-or-maximum-transaction-by-customer-id)

Supported window aggregate functions are listed in the following table.

<table><thead><tr><th>Function</th><th>Description</th><th width="198">Example</th><th>Default Value When No Record Selected</th></tr></thead><tbody><tr><td><a href="https://github.com/pinot-contrib/pinot-docs/blob/master/configuration-reference/functions/avg.md"><strong>AVG</strong></a></td><td>Returns the average of the values for a numeric column as a<code>Double over the specified number of rows or partition (if applicable).</code></td><td><code>AVG(playerScore)</code></td><td><code>Double.NEGATIVE_INFINITY</code></td></tr><tr><td>BOOL_AND</td><td>Returns true if all input values are true, otherwise false</td><td></td><td></td></tr><tr><td>BOOL_OR</td><td>Returns true if at least one input value is true, otherwise false</td><td></td><td></td></tr><tr><td><a href="../../../configuration-reference/functions/count.md"><strong>COUNT</strong></a></td><td>Returns the count of the records as <code>Long</code></td><td><code>COUNT(*)</code></td><td><code>0</code></td></tr><tr><td><a href="../../../configuration-reference/functions/min.md"><strong>MIN</strong></a></td><td>Returns the minimum value of a numeric column as <code>Double</code></td><td><code>MIN(playerScore)</code></td><td><code>Double.POSITIVE_INFINITY</code></td></tr><tr><td><a href="../../../configuration-reference/functions/max.md"><strong>MAX</strong></a></td><td>Returns the maximum value of a numeric column as <code>Double</code></td><td><code>MAX(playerScore)</code></td><td><code>Double.NEGATIVE_INFINITY</code></td></tr><tr><td><a href="../../../configuration-reference/functions/round-1-1.md"><strong>ROW_NUMBER</strong></a></td><td>Assigns a unique row number to all the rows in a specified table.</td><td><code>ROW_NUMBER()</code></td><td><code>0</code></td></tr><tr><td><a href="../../../configuration-reference/functions/sum.md"><strong>SUM</strong></a></td><td>Returns the sum of the values for a numeric column as <code>Double</code></td><td><code>SUM(playerScore)</code></td><td><code>0</code></td></tr><tr><td><a href="../../../configuration-reference/functions/lead.md">LEAD</a></td><td>The <code>LEAD</code> function provides access to a subsequent row within the same result set, without the need for a self-join.</td><td><code>LEAD(column_name, offset, default_value)</code></td><td></td></tr><tr><td><a href="../../../configuration-reference/functions/lag.md">LAG</a></td><td>The <code>LAG</code> function provides access to a previous row within the same result set, without the need for a self-join.</td><td><code>LAG(column_name, offset, default_value)</code></td><td></td></tr><tr><td>FIRST_VALUE</td><td>The <code>FIRST_VALUE</code> function returns the first value in an ordered set of values within the window frame.</td><td><code>FIRST_VALUE(salary)</code></td><td></td></tr><tr><td>LAST_VALUE</td><td>The <code>LAST_VALUE</code> function returns the last value in an ordered set of values within the window frame.</td><td><code>LAST_VALUE(salary)</code></td><td></td></tr></tbody></table>

## Window aggregate query examples

* [Sum transactions by customer ID](windows-functions.md#sum-transactions-by-customer-id)
* [Find the minimum or maximum transaction by customer ID](windows-functions.md#find-the-minimum-or-maximum-transaction-by-customer-id)
* [Find the average transaction amount by customer ID](windows-functions.md#find-the-average-transaction-amount-by-customer-id)
* [Rank year-to-date sales for a sales team](windows-functions.md#rank-year-to-date-sales-for-a-sales-team)
* [Count the number of transactions by customer ID](windows-functions.md#count-the-number-of-transactions-by-customer-id)

### Sum transactions by customer ID

Calculate the rolling sum transaction amount ordered by the payment date for each customer ID (note, the default frame here is UNBOUNDED PRECEDING and CURRENT ROW).

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

Calculate the least (use `MIN()`) or most expensive (use `MAX()`) transaction made by each customer comparing all transactions made by the customer (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING). The following query shows how to find the least expensive transaction.

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, MIN(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

<table><thead><tr><th>customer_id</th><th width="224">payment_date</th><th width="160">amount</th><th data-type="number">min</th></tr></thead><tbody><tr><td>1</td><td>2023-02-14 23:22:38.996577</td><td>5.99</td><td>0.99</td></tr><tr><td>1</td><td>2023-02-15 16:31:19.996577</td><td>0.99</td><td>0.99</td></tr><tr><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td><td>0.99</td></tr><tr><td>2</td><td>2023-04-30 04:34:36.996577</td><td>4.99</td><td>4.99</td></tr><tr><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td><td>4.99</td></tr><tr><td>3</td><td>2023-03-23 05:38:40.996577</td><td>2.99</td><td>2.99</td></tr><tr><td>3</td><td>2023-04-07 08:51:51.996577</td><td>3.99</td><td>2.99</td></tr><tr><td>3</td><td>3 | 2023-04-08 11:15:37.996577</td><td>4.99</td><td>2.99</td></tr></tbody></table>

### Find the average transaction amount by customer ID

Calculate a customer’s average transaction amount for all transactions they’ve made (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, AVG(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

<table><thead><tr><th>customer_id</th><th>payment_date</th><th width="131">amount</th><th data-type="number">avg</th></tr></thead><tbody><tr><td>1</td><td>2023-02-14 23:22:38.996577</td><td>5.99</td><td>5.66</td></tr><tr><td>1</td><td>2023-02-15 16:31:19.996577</td><td>0.99</td><td>5.66</td></tr><tr><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td><td>5.66</td></tr><tr><td>2</td><td>2023-04-30 04:34:36.996577</td><td>4.99</td><td>7.99</td></tr><tr><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td><td>7.99</td></tr><tr><td>3</td><td>2023-03-23 05:38:40.996577</td><td>2.99</td><td>3.99</td></tr><tr><td>3</td><td>2023-04-07 08:51:51.996577</td><td>3.99</td><td>3.99</td></tr><tr><td>3</td><td>2023-04-08 11:15:37.996577</td><td>4.99</td><td>3.99</td></tr></tbody></table>

### Rank year-to-date sales for a sales team

Use `ROW_NUMBER()` to rank team members by their year-to-date sales (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

{% code overflow="wrap" %}
```sql
SELECT ROW_NUMBER() OVER(ORDER BY SalesYTD DESC) AS Row,   
    FirstName, LastName AS "Total sales YTD"   
FROM Sales.vSalesPerson;  
```
{% endcode %}

<table><thead><tr><th>Row</th><th width="257">FirstName</th><th width="122">LastName</th><th data-type="number">Total sales YTD</th></tr></thead><tbody><tr><td>1</td><td>Joe</td><td>Smith</td><td>2251368.34</td></tr><tr><td>2</td><td>Alice</td><td>Davis</td><td>2151341.64</td></tr><tr><td>3</td><td>James</td><td>Jones</td><td>1551363.54</td></tr><tr><td>4</td><td>Dane</td><td>Scott</td><td>1251358.72</td></tr></tbody></table>

### Count the number of transactions by customer ID

Count the number of transactions made by each customer (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

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
