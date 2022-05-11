---
description: This section contains reference documentation for the sumprecision function.
---

# sumprecision

Get the sum of values in a group with optional precision and optional scale. This function is used for BigDecimal calculations.

## Signature

> SUMPRECISION(colName)
> SUMPRECISION(colName, precision, scale)

precision (optional): precision to be set to the final result.
scale (optional): scale to be set to the final result.

## Usage Examples

```sql
select sumprecision(salary, 10, 4) AS value
from employees
```
