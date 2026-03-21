---
description: >-
  This section contains reference documentation for the arrayUnionString
  function.
---

# arrayUnionString

Create a union of two arrays of strings.

## Signature

> arrayUnionString('colName1', 'colName2')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivTailNums, 
       DivAirports,
       arrayUnionString(DivTailNums, DivAirports) AS unionIds
from airlineStats 
WHERE arraylength(DivTailNums) >= 2
limit 5
```

| DivTailNums   | DivAirports | unionIds       |
| ------------- | ----------- | -------------- |
| N7713A,N7713A | IND,IND     | N7713A,IND     |
| N344AA,N344AA | MCI,BOS     | N344AA,MCI,BOS |
| N7713A,N7713A | IND,IND     | N7713A,IND     |
| N344AA,N344AA | MCI,BOS     | N344AA,MCI,BOS |
