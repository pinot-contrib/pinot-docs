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

| sales\_date | sales\_amount | next\_day\_sales |
| ----------- | ------------- | ---------------- |
| 2023-02-14  | 200           | 180              |
| 2023-02-15  | 180           | 220              |
| 2023-02-16  | 220           | NULL             |

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

| transaction\_id | payment\_date              | amount | next\_payment\_amount |
| --------------- | -------------------------- | ------ | --------------------- |
| 416             | 2023-02-14 21:21:59.996577 | 2.99   | 4.99                  |
| 516             | 2023-02-14 21:23:39.996577 | 4.99   | 4.99                  |
| 239             | 2023-02-14 21:29:00.996577 | 4.99   | 6.99                  |

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

| month | year | expenses | next\_month\_expenses |
| ----- | ---- | -------- | --------------------- |
| 1     | 2023 | 1000     | 1100                  |
| 2     | 2023 | 1100     | 1200                  |
| 3     | 2023 | 1200     | NULL                  |

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

<figure><img src="../../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>
