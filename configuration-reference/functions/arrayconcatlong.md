---
description: >-
  This section contains reference documentation for the arrayConcatLong
  function.
---

# arrayConcatLong

Concatenates two arrays of longs.

## Signature

> arrayConcatLong('colName1', 'colName2')

## Usage Examples

This example assumes the multiValueTable columns mvCol1 and mvCol2 are both of type LONG with singleValueField in the table schema set to false.

```sql
select mvCol1, 
       arrayConcatLong(mvCol1, mvCol2) AS concatLongs
from multiValueTable
WHERE arraylength(mvCol1) >= 2
limit 5
```
