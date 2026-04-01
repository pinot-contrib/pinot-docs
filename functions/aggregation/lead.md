---
description: This section contains reference documentation for the LEAD function.
---

# LEAD

Returns the value from a following row in the same result set, based on a specified physical offset. It can be used to compare values in the current row with values in a subsequent row.

### Signature

```sql
LEAD(any expression [, bigint offset [, any default]])
```

### Arguments

* expression: The column or calculation from which the value is to be returned.
* offset: The number of rows before the current row from which to retrieve the value. The default is 1 if not specified.
* default: The value to return if the offset goes beyond the scope of the window. If not specified, NULL is returned.

### Example

Forecast next day's sales based on current data.

Anticipate the next payment amount for budget planning.

Identify potential increases in expenses or revenue.

Forecast next day's sales based on current data This example shows how to use the LEAD function to anticipate sales for the next day.

```sql
SELECT
    sales_date,
    sales_amount,
    LEAD(sales_amount, 1) OVER (ORDER BY sales_date) AS next_day_sales
FROM
    daily_sales;
```

Output:

<table>
  <thead>
    <tr>
      <th>sales\_date</th>
      <th>sales\_amount</th>
      <th>next\_day\_sales</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2023-02-14</td>
      <td>200</td>
      <td>180</td>
    </tr>
    <tr>
      <td>2023-02-15</td>
      <td>180</td>
      <td>220</td>
    </tr>
    <tr>
      <td>2023-02-16</td>
      <td>220</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>

Anticipate the next payment amount for budget planning This query retrieves the next payment amount for each transaction to assist in financial forecasting and budgeting.

```sql
SELECT
    transaction_id,
    payment_date,
    amount,
    LEAD(amount, 1) OVER (ORDER BY payment_date) AS next_payment_amount
FROM
    payments;
```

Output:

<table>
  <thead>
    <tr>
      <th>transaction\_id</th>
      <th>payment\_date</th>
      <th>amount</th>
      <th>next\_payment\_amount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>416</td>
      <td>2023-02-14 21:21:59.996577</td>
      <td>2.99</td>
      <td>4.99</td>
    </tr>
    <tr>
      <td>516</td>
      <td>2023-02-14 21:23:39.996577</td>
      <td>4.99</td>
      <td>4.99</td>
    </tr>
    <tr>
      <td>239</td>
      <td>2023-02-14 21:29:00.996577</td>
      <td>4.99</td>
      <td>6.99</td>
    </tr>
  </tbody>
</table>

Identify potential increases in expenses or revenue Utilize the LEAD function to examine monthly data and predict potential increases or trends in expenses or revenue for future planning.

```sql
SELECT
    month,
    year,
    expenses,
    LEAD(expenses, 1) OVER (ORDER BY year, month) AS next_month_expenses
FROM
    financials;
```

Output:

<table>
  <thead>
    <tr>
      <th>month</th>
      <th>year</th>
      <th>expenses</th>
      <th>next\_month\_expenses</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2023</td>
      <td>1000</td>
      <td>1100</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2023</td>
      <td>1100</td>
      <td>1200</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2023</td>
      <td>1200</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>

Use with CTE:

```sql
WITH tmp AS (
  select count(*) as num_trips,
    DaysSinceEpoch
  from airlineStats
  GROUP BY DaysSinceEpoch
)

SELECT DaysSinceEpoch,
  num_trips,
  LEAD(num_trips, 2) OVER (
    ORDER BY DaysSinceEpoch
  ) AS previous_num_trips,
  num_trips - LEAD(num_trips, 2) OVER (
    ORDER BY DaysSinceEpoch
  ) AS difference
FROM tmp;
```

<figure><img src="../.gitbook/assets/image (1) (1) (1) (1).png" alt=""><figcaption></figcaption></figure>
