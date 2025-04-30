---
description: This section contains reference documentation for the arrayUnionInt function.
---

# arrayUnionInt

Create a union of two arrays of ints.

## Signature

> arrayUnionInt('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivWheelsOffs, 
       DivWheelsOns,
       arrayUnionInt(DivWheelsOffs, DivWheelsOns) AS unionIds
from airlineStats 
WHERE arraylength(DivWheelsOffs) >= 2
limit 5
```

| DivWheelsOffs | DivWheelsOns | unionIds            |
| ------------- | ------------ | ------------------- |
| 1453,1731     | 1415,1623    | 1453,1731,1415,1623 |
| 1908,1758     | 1339,2310    | 1908,1758,1339,2310 |
| 1453,1731     | 1415,1623    | 1453,1731,1415,1623 |
| 1908,1758     | 1339,2310    | 1908,1758,1339,2310 |
