---
description: >-
  Use window functions to compute averages, sort, rank, or count items,
  calculate sums, and find minimum or maximum values.
---

# Window functions

{% hint style="info" %}
**Important:** To query using Windows functions, you must [use Pinot's multi-stage query engine (v2).](../../../developers/advanced/v2-multi-stage-query-engine.md)
{% endhint %}

Use window functions to do the following:

* [Compute averages](windows-functions.md#find-the-average-transaction-amount-by-customer-id)
* [Rank items](windows-functions.md#rank-year-to-date-sales-for-a-sales-team)
* [Calculate sums](windows-functions.md#sum-transactions-by-customer-id)
* [Find minimum or maximum values](windows-functions.md#find-the-minimum-or-maximum-transaction-by-customer-id)

### Window functions overview

* Window functions consist of a supported function and an [OVER clause](windows-functions.md#over-clause).&#x20;
* To learn more about syntax, see [Windows function query syntax](windows-functions.md#window-function-query-syntax), and read about the [OVER clause](windows-functions.md#over-clause).&#x20;
* To see Windows functions you can use in Pinot, see [Supported Pinot window functions](windows-functions.md#supported-pinot-window-functions).
* To query with Windows functions in Pinot, see [examples for supported Windows functions.](windows-functions.md#examples-of-windows-functions)

## Window function query syntax

For information about the Window function query syntax, see [Calcite documentation](https://calcite.apache.org/docs/reference.html#window-functions).

### Example query layout

The following query shows the complete components of the window function. Note, `PARTITION BY` and `ORDER BY` are optional.

{% code overflow="wrap" %}
```sql
SELECT FUNC(column1) OVER (PARTITION BY column2 ORDER BY column3 ROWS 2 PRECEDING)
    FROM tableName
    WHERE filter_clause  
```
{% endcode %}

## OVER clause

#### Partition by clause

* If a PARTITION BY clause is specified, the intermediate results will be grouped into different partitions based on the values of the columns appearing in the PARTITION BY clause.
* If the PARTITION BY clause isn’t specified, the whole result will be regarded as one big partition, i.e. there is only one partition in the result set.

#### Order by clause

* If an ORDER BY clause is specified, all the rows within the same partition will be sorted based on the values of the columns appearing in the window ORDER BY clause. The ORDER BY clause decides the order in which the rows within a partition are to be processed.
* If no ORDER BY clause is specified while a PARTITION BY clause is specified, the order of the rows is undefined. If output ordering is desired a global ORDER BY clause should be used in the query.

#### Frame clause

* {RANGE|ROWS} frame\_start OR
* {RANGE|ROWS} BETWEEN frame\_start AND frame\_end; frame\_start and frame\_end can be any of:
  * UNBOUNDED PRECEDING: expression PRECEDING. May only be allowed in ROWS mode \[depends on DB, some support some don’t]
  * CURRENT ROW expression FOLLOWING. May only be allowed in ROWS mode \[depends on DB, some support some don’t]
  * UNBOUNDED FOLLOWING:
    * If no FRAME clause is specified, then the default frame behavior depends on whether ORDER BY is present or not.&#x20;
    * If an ORDER BY clause is specified, the default behavior is to calculate the aggregation from the beginning of the partition to the current row or UNBOUNDED PRECEDING to CURRENT ROW.
    * If only a PARTITION BY clause is present, the default frame behavior is to calculate the aggregation from UNBOUNDED PRECEDING to CURRENT ROW.

If there is no FRAME, no PARTITION BY, and no ORDER BY clause specified in the OVER clause (empty OVER), the whole result set is regarded as one partition, and there's one frame in the window.

The OVER clause applies a specified[ supported Windows function](windows-functions.md#supported-pinot-window-functions) to compute values over a group of rows, and return a single result for each row. The OVER clause specifies how the rows are arranged and how the aggregation is done on those rows.

Inside the over clause, there are three optional components, i.e. PARTITION BY clause, ORDER BY clause, and FRAME clause.

## Supported Pinot window functions



| Function                                                                                                    | Description                                                                                                                         | Example            | Default Value When No Record Selected |
| ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ------------------------------------- |
| [**AVG**](https://github.com/pinot-contrib/pinot-docs/blob/master/configuration-reference/functions/avg.md) | Returns the average of the values for a numeric column as a`Double over the specified number of rows or partition (if applicable).` | `AVG(playerScore)` | `Double.NEGATIVE_INFINITY`            |
| BOOL\_AND                                                                                                   | Returns true if all input values are true, otherwise false                                                                          |                    |                                       |
| BOOL\_OR                                                                                                    | Returns true if at least one input value is true, otherwise false                                                                   |                    |                                       |
| [**COUNT**](../../../configuration-reference/functions/count.md)                                            | Returns the count of the records as `Long`                                                                                          | `COUNT(*)`         | `0`                                   |
| [**MIN**](../../../configuration-reference/functions/min.md)                                                | Returns the minimum value of a numeric column as `Double`                                                                           | `MIN(playerScore)` | `Double.POSITIVE_INFINITY`            |
| [**MAX**](../../../configuration-reference/functions/max.md)                                                | Returns the maximum value of a numeric column as `Double`                                                                           | `MAX(playerScore)` | `Double.NEGATIVE_INFINITY`            |
| [**ROW\_NUMBER**](../../../configuration-reference/functions/round-1.md)                                    | Assigns a unique row number to all the rows in a specified table.                                                                   | `ROW_NUMBER()`     | `0`                                   |
| [**SUM**](../../../configuration-reference/functions/sum.md)                                                | Returns the sum of the values for a numeric column as `Double`                                                                      | `SUM(playerScore)` | `0`                                   |

## Examples of windows functions

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

|  customer\_id  |   payment\_date             | amount   |  sum   |
| -------------- | --------------------------- | -------- | ------ |
| 1              | 2023-02-14 23:22:38.996577  | 5.99     | 5.99   |
| 1              |  2023-02-15 16:31:19.996577 | 0.99     |  6.98  |
| 1              | 2023-02-15 19:37:12.996577  | 9.99     |  16.97 |
| 1              | 2023-02-16 13:47:23.996577  | 4.99     |  21.96 |
| 2              | 2023-02-17 19:23:24.996577  | 2.99     | 2.99   |
| 2              | 2023-02-17 19:23:24.996577  | 0.99     | 3.98   |
| 3              | 2023-02-16 00:02:31.996577  | 8.99     | 8.99   |
| 3              | 2023-02-16 13:47:36.996577  |  6.99    | 15.98  |
| 3              | 2023-02-17 03:43:41.996577  | 6.99     | 22.97  |
| 4              | 2023-02-15 07:59:54.996577  | 4.99     | 4.99   |
| 4              | 2023-02-16 06:37:06.996577  | 0.99     | 5.98   |

### Find the minimum or maximum transaction by customer ID

Calculate the least (use `MIN()`) or most expensive (use `MAX()`) transaction made by each customer comparing all transactions made by the customer (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING). The following query shows how to find the least expensive transaction.&#x20;

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, MIN(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

<table><thead><tr><th>customer_id</th><th width="224">payment_date </th><th width="160">amount</th><th data-type="number">min</th></tr></thead><tbody><tr><td>1</td><td>2023-02-14 23:22:38.996577</td><td> 5.99</td><td>0.99</td></tr><tr><td>1</td><td>2023-02-15 16:31:19.996577</td><td>0.99 </td><td>0.99</td></tr><tr><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td><td>0.99</td></tr><tr><td>2</td><td>2023-04-30 04:34:36.996577</td><td>4.99</td><td>4.99</td></tr><tr><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td><td>4.99</td></tr><tr><td>3</td><td>2023-03-23 05:38:40.996577 </td><td>2.99</td><td>2.99</td></tr><tr><td>3</td><td> 2023-04-07 08:51:51.996577</td><td>3.99 </td><td>2.99</td></tr><tr><td>3</td><td>3 | 2023-04-08 11:15:37.996577</td><td>4.99 </td><td>2.99</td></tr></tbody></table>

### Find the average transaction amount by customer ID

Calculate a customer’s average transaction amount for all transactions they’ve made (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).

{% code overflow="wrap" %}
```sql
SELECT customer_id, payment_date, amount, AVG(amount) OVER(PARTITION BY customer_id) from payment;
```
{% endcode %}

<table><thead><tr><th>customer_id</th><th>payment_date </th><th width="131">amount</th><th data-type="number">avg</th></tr></thead><tbody><tr><td>1</td><td>2023-02-14 23:22:38.996577</td><td> 5.99</td><td>5.66</td></tr><tr><td>1</td><td>2023-02-15 16:31:19.996577</td><td>0.99 </td><td>5.66</td></tr><tr><td>1</td><td>2023-02-15 19:37:12.996577</td><td>9.99</td><td>5.66</td></tr><tr><td>2</td><td>2023-04-30 04:34:36.996577</td><td>4.99</td><td>7.99</td></tr><tr><td>2</td><td>2023-04-30 12:16:09.996577</td><td>10.99</td><td>7.99</td></tr><tr><td>3</td><td>2023-03-23 05:38:40.996577 </td><td>2.99</td><td>3.99</td></tr><tr><td>3</td><td>2023-04-07 08:51:51.996577</td><td>3.99 </td><td>3.99</td></tr><tr><td>3</td><td>2023-04-08 11:15:37.996577</td><td>4.99 </td><td>3.99</td></tr></tbody></table>

### Rank year-to-date sales for a sales team

Use `ROW_NUMBER()` to rank team members by their year-to-date sales (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).&#x20;

{% code overflow="wrap" %}
```sql
SELECT ROW_NUMBER() OVER(ORDER BY SalesYTD DESC) AS Row,   
    FirstName, LastName AS "Total sales YTD"   
FROM Sales.vSalesPerson;  
```
{% endcode %}

<table><thead><tr><th>Row</th><th width="257">FirstName</th><th width="122">LastName</th><th data-type="number">Total sales YTD</th></tr></thead><tbody><tr><td>1</td><td>Joe</td><td>Smith</td><td>2251368.34</td></tr><tr><td>2</td><td>Alice </td><td>Davis</td><td>2151341.64</td></tr><tr><td>3</td><td>James</td><td>Jones</td><td>1551363.54</td></tr><tr><td>4</td><td>Dane</td><td>Scott</td><td>1251358.72</td></tr></tbody></table>

### Count the number of transactions by customer ID

Count the number of transactions made by each customer (default frame here is UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING).&#x20;

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
