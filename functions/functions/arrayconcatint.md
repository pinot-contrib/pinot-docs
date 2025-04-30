---
description: This section contains reference documentation for the arrayConcatInt function.
---

# arrayConcatInt

Concatenates two arrays of ints.

## Signature

> arrayConcatInt('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivWheelsOffs, 
       arrayConcatInt(DivWheelsOffs, DivWheelsOns) AS concatIds
from airlineStats 
WHERE arraylength(DivWheelsOffs) >= 2
limit 5
```

| DivWheelsOffs | concatIds           |
| ------------- | ------------------- |
| 1453,1731     | 1453,1731,1415,1623 |
| 1908,1758     | 1908,1758,1339,2310 |
| 1453,1731     | 1453,1731,1415,1623 |
| 1908,1758     | 1908,1758,1339,2310 |
