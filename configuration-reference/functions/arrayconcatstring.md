---
description: This section contains reference documentation for the arrayConcatString function.
---

# arrayConcatString

Concatenates two arrays of strings.

## Signature

> arrayConcatString('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select DivTailNums, 
       arrayConcatString(DivTailNums, DivTailNums) AS concatIds
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

|DivTailNums|	concatIds|
| ------------- | ------------- |
|N7713A,N7713A	|N7713A,N7713A,N7713A,N7713A|
|N344AA,N344AA	|N344AA,N344AA,N344AA,N344AA|
|N344AA,N344AA	|N344AA,N344AA,N344AA,N344AA|
|N7713A,N7713A	|N7713A,N7713A,N7713A,N7713A|