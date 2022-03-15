---
description: This section contains reference documentation for the arrayContainsString function.
---

# arrayContainsString

Checks if string value exists in array.

## Signature

> arrayContainsString('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select DivTailNums, 
       arrayContainsString(DivTailNums, 'N7713A') AS index
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

| DivTailNums	|index|
| ------------- | ------------- |
|N7713A,N7713A|	true|
|N344AA,N344AA|	false|
|N7713A,N7713A|	true|