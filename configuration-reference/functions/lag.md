---
description: This section contains reference documentation for the LAG function.
---

# LAG

Returns the value from a preceding row in the same result set, based on a specified physical offset. It can be used to compare values in the current row with values in a previous row.

### Signature

```sql
LAG(any expression [, bigint offset [, any default]])
```

### Arguments

* expression: The column or calculation from which the value is to be returned.
* offset: The number of rows before the current row from which to retrieve the value. The default is 1 if not specified.
* default: The value to return if the offset goes beyond the scope of the window. If not specified, NULL is returned.

### Example

This example calculates the difference in sales between the current day and the previous day.

Retrieve the previous payment amount for comparison.

Identify trends by comparing current data with historical data.

Calculate the difference in sales between the current day and the previous day This example shows how to use the LAG function to find the sales difference between consecutive days.

```sql
SELECT
    sales_date,
    sales_amount,
    LAG(sales_amount, 1) OVER (ORDER BY sales_date) AS previous_day_sales,
    sales_amount - LAG(sales_amount, 1) OVER (ORDER BY sales_date) AS difference
FROM
    daily_sales;
```

Output:

<table data-full-width="false"><thead><tr><th>sales_date</th><th>sales_amount</th><th>previous_day_sales</th><th>difference</th></tr></thead><tbody><tr><td>2023-02-14</td><td>200</td><td>NULL</td><td>NULL</td></tr><tr><td>2023-02-15</td><td>180</td><td>200</td><td>-20</td></tr><tr><td>2023-02-16</td><td>220</td><td>180</td><td>40</td></tr></tbody></table>

Retrieve the previous payment amount for comparison This query retrieves the last payment amount for each payment to see if the amount is increasing or decreasing.

```sql
SELECT
    payment_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY payment_date) AS previous_amount
FROM
    payment;
```

Output:

| payment\_date              | amount | previous\_amount |
| -------------------------- | ------ | ---------------- |
| 2023-02-14 21:21:59.996577 | 2.99   | NULL             |
| 2023-02-14 21:23:39.996577 | 4.99   | 2.99             |
| 2023-02-14 21:29:00.996577 | 4.99   | 4.99             |

Identify trends by comparing current data with historical data Use the LAG function to compare the current month's data with the same month from the previous year to identify trends or significant changes.

```sql
SELECT
    month,
    year,
    data_value,
    LAG(data_value, 12) OVER (ORDER BY year, month) AS previous_year_data
FROM
    monthly_data;
```

Output:

| month | year | data\_value | previous\_year\_data |
| ----- | ---- | ----------- | -------------------- |
| 1     | 2023 | 150         | NULL                 |
| 1     | 2024 | 170         | 150                  |



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
  LAG(num_trips, 2) OVER (
    ORDER BY DaysSinceEpoch
  ) AS previous_num_trips,
  num_trips - LAG(num_trips, 2) OVER (
    ORDER BY DaysSinceEpoch
  ) AS difference
FROM tmp;
```

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption><p>CTE based LAG query</p></figcaption></figure>
