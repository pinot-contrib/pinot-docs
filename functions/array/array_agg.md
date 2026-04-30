---
description: This section contains reference documentation for the ARRAY_AGG function.
---

# ARRAY\_AGG

Concatenates the input values into an array. Supported element types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `STRING`, and `BYTES`.



## Signature

> ARRAY\_AGG(dataColumn, 'dataType', \[isDistinct])



## Usage Examples

```sql
SELECT ARRAY_AGG(firstName, 'STRING', true) AS firstNames from transcript;
```

| firstNames    |
| ------------- |
| Bob,Nick,Lucy |

When the input expression is multi-value, Pinot flattens the per-row values into the output array before applying the optional distinct step.
