---
description: This section contains reference documentation for the DENSE_RANK window function.
---

# DENSE_RANK

Returns the rank of the current row within its partition, without gaps for ties.

`DENSE_RANK()` assigns the same rank to peer rows that compare equal under the window's `ORDER BY` clause. The next distinct value gets the next consecutive rank.

## Signature

```sql
DENSE_RANK()
```

## Usage Notes

* `DENSE_RANK()` takes no arguments.
* Ranking restarts for each `PARTITION BY` group.
* The row ranking is determined by the window's `ORDER BY` clause.
* Equal rows receive the same rank, and subsequent ranks remain consecutive.
* No explicit window frame clause can be specified for `DENSE_RANK()`.

## Examples

Rank salespeople by year-to-date sales without leaving gaps when values tie.

```sql
SELECT
    FirstName,
    LastName,
    SalesYTD,
    DENSE_RANK() OVER (ORDER BY SalesYTD DESC) AS sales_rank
FROM Sales.vSalesPerson;
```

Output:

| FirstName | LastName | SalesYTD | sales_rank |
| --- | --- | --- | --- |
| Joe | Smith | 2251368.34 | 1 |
| Alice | Davis | 2151341.64 | 2 |
| James | Jones | 2151341.64 | 2 |
| Dane | Scott | 1251358.72 | 3 |

Rank employees within each department by salary using consecutive ranks.

```sql
SELECT
    department,
    employee_name,
    salary,
    DENSE_RANK() OVER (
        PARTITION BY department
        ORDER BY salary DESC
    ) AS salary_rank
FROM employees;
```

Output:

| department | employee_name | salary | salary_rank |
| --- | --- | --- | --- |
| Engineering | Alice | 160000 | 1 |
| Engineering | Bob | 150000 | 2 |
| Engineering | Carol | 150000 | 2 |
| Engineering | Dave | 140000 | 3 |
| Sales | Eve | 130000 | 1 |
| Sales | Frank | 120000 | 2 |

## Related Pages

* [Window Functions](README.md)
* [ROW_NUMBER](row_number.md)
* [RANK](rank.md)
* [Function Index](../../build-with-pinot/querying-and-sql/function-index.md)
