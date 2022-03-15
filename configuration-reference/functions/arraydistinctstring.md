---
description: This section contains reference documentation for the arrayDistinctString function.
---

# arrayDistinctString

Returns unique values in an array of strings.

## Signature

> arrayDistinctString('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select DivTailNums, 
       arrayDistinctString(DivTailNums) AS unique
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

| DivTailNums	|unique|
| ------------- | ------------- |
|N7713A,N7713A	|N7713A| 
|N344AA,N344AA	|N344AA|
|N344AA,N344AA	|N344AA|
|N7713A,N7713A	|N7713A|