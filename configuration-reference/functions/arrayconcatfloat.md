---
description: This section contains reference documentation for the arrayConcatFloat function.
---

# arrayConcatFloat

Concatenates two arrays of floats.

## Signature

> arrayConcatFloat('colName1', 'colName2')

## Usage Examples

This example assumes the multiValueTable columns mvCol1 and mvCol2 are both of type FLOAT with
singleValueField in the table schema set to false.


```sql
select mvCol1, 
       arrayConcatFloat(mvCol1, mvCol2) AS concatFloats
from multiValueTable
WHERE arraylength(mvCol1) >= 2
limit 5
```
