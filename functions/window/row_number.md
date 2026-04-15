---
description: This section contains reference documentation for the ROW_NUMBER window function.
---

# ROW_NUMBER

Returns the sequential number of the current row within its partition, counting from 1.

`ROW_NUMBER()` is commonly used to rank rows after sorting them inside each partition. For deterministic results, specify an `ORDER BY` clause in the window definition.

## Signature

```sql
ROW_NUMBER()
```

## Usage Notes

* `ROW_NUMBER()` takes no arguments.
* Numbering restarts for each `PARTITION BY` group.
* The row order is determined by the window's `ORDER BY` clause.
* No explicit window frame clause can be specified for `ROW_NUMBER()`.

## Examples

Assign a row number to each salesperson by year-to-date sales.

```sql
SELECT
    ROW_NUMBER() OVER (ORDER BY SalesYTD DESC) AS Row,
    FirstName,
    LastName,
    SalesYTD AS "Total sales YTD"
FROM Sales.vSalesPerson;
```

Output:

| Row | FirstName | LastName | Total sales YTD |
| --- | --- | --- | --- |
| 1 | Joe | Smith | 2251368.34 |
| 2 | Alice | Davis | 2151341.64 |
| 3 | James | Jones | 1551363.54 |
| 4 | Dane | Scott | 1251358.72 |

Assign a row number within each customer partition, ordered by payment time.

```sql
SELECT
    customer_id,
    payment_date,
    amount,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY payment_date
    ) AS payment_number
FROM payment;
```

Output:

| customer_id | payment_date | amount | payment_number |
| --- | --- | --- | --- |
| 1 | 2023-02-14 23:22:38.996577 | 5.99 | 1 |
| 1 | 2023-02-15 16:31:19.996577 | 0.99 | 2 |
| 1 | 2023-02-15 19:37:12.996577 | 9.99 | 3 |
| 2 | 2023-02-17 19:23:24.996577 | 2.99 | 1 |
| 2 | 2023-02-17 19:24:10.996577 | 0.99 | 2 |

## Related Pages

* [Window Functions](README.md)
* [Function Index](../../build-with-pinot/querying-and-sql/function-index.md)
