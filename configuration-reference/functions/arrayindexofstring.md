---
description: This section contains reference documentation for the arrayIndexOfString function.
---

# arrayIndexOfString

Finds the last index of the given value in the array starting at the given index.

## Signature

> arrayIndexOfString('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select DivTailNums, 
       arrayIndexOfString(DivTailNums, 'N7713A') AS index
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

| DivTailNums	|index|
| ------------- | ------------- |
|N7713A,N7713A|	0|
|N344AA,N344AA|	-1|
|N7713A,N7713A|	0|