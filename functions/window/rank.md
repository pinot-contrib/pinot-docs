---
description: This section contains reference documentation for the RANK window function.
---

# RANK

Returns the rank of the current row within its partition, with gaps for ties.

`RANK()` assigns the same rank to peer rows that compare equal under the window's `ORDER BY` clause. The next rank then skips ahead by the number of tied rows.

## Signature

```sql
RANK()
```

## Usage Notes

* `RANK()` takes no arguments.
* Ranking restarts for each `PARTITION BY` group.
* The row ranking is determined by the window's `ORDER BY` clause.
* Equal rows receive the same rank, and subsequent ranks contain gaps.
* No explicit window frame clause can be specified for `RANK()`.

## Examples

Rank salespeople by year-to-date sales, leaving gaps when values tie.

```sql
SELECT
    FirstName,
    LastName,
    SalesYTD,
    RANK() OVER (ORDER BY SalesYTD DESC) AS sales_rank
FROM Sales.vSalesPerson;
```

Output:

| FirstName | LastName | SalesYTD | sales_rank |
| --- | --- | --- | --- |
| Joe | Smith | 2251368.34 | 1 |
| Alice | Davis | 2151341.64 | 2 |
| James | Jones | 2151341.64 | 2 |
| Dane | Scott | 1251358.72 | 4 |

Rank employees within each department by salary.

```sql
SELECT
    department,
    employee_name,
    salary,
    RANK() OVER (
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
| Engineering | Dave | 140000 | 4 |
| Sales | Eve | 130000 | 1 |
| Sales | Frank | 120000 | 2 |

## Related Pages

* [Window Functions](README.md)
* [ROW_NUMBER](row_number.md)
* [DENSE_RANK](dense_rank.md)
* [Function Index](../../build-with-pinot/querying-and-sql/function-index.md)
