---
description: This section contains reference documentation for the ARRAY_AGG function.
---

# ARRAY\_AGG

Concatenates the input values into an array.



## Signature

> ARRAY\_AGG(dataColumn, 'dataType', \[isDistinct])



## Usage Examples

```sql
SELECT ARRAY_AGG(firstName, 'STRING', true) AS firstNames from transcript;
```



| firstNames    |
| ------------- |
| Bob,Nick,Lucy |
