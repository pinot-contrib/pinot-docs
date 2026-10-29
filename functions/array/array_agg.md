---
description: This section contains reference documentation for the ARRAY_AGG function.
---

# ARRAY\_AGG

Concatenates the input values into an array. Supported element types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `STRING`, and `BYTES`.



## Signature

> ARRAY\_AGG(dataColumn\[, 'dataType']\[, isDistinct])
>
> ARRAY\_AGG(DISTINCT dataColumn)

The `dataType` argument is optional. When it is omitted, Pinot infers it from the type of `dataColumn` (the element type for a multi-value column). Distinct values can be collected either with the `DISTINCT` keyword inside the call or with the trailing `isDistinct` boolean argument.



## Usage Examples

```sql
SELECT ARRAY_AGG(firstName, 'STRING', true) AS firstNames from transcript;
```

The `dataType` argument can be omitted, and `DISTINCT` can be written as a keyword:

```sql
SELECT ARRAY_AGG(DISTINCT firstName) AS firstNames from transcript;
```

| firstNames    |
| ------------- |
| Bob,Nick,Lucy |

When the input expression is multi-value, Pinot flattens the per-row values into the output array before applying the optional distinct step.
