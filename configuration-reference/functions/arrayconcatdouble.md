---
description: >-
  This section contains reference documentation for the arrayConcatDouble
  function.
---

# arrayConcatDouble

Concatenates two arrays of doubles.

## Signature

> arrayConcatDouble('colName1', 'colName2')

## Usage Examples

This example assumes the multiValueTable columns mvCol1 and mvCol2 are both of type DOUBLE with singleValueField in the table schema set to false.

```sql
select mvCol1, 
       arrayConcatDouble(mvCol1, mvCol2) AS concatDoubles
from multiValueTable
WHERE arraylength(mvCol1) >= 2
limit 5
```
