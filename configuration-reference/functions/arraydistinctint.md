---
description: >-
  This section contains reference documentation for the arrayDistinctInt
  function.
---

# arrayDistinctInt

Returns unique values in an array of ints.

## Signature

> arrayDistinctInt('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayDistinctInt(DivAirportIDs) AS unique
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

| DivAirportIDs | unique      |
| ------------- | ----------- |
| 15016,11066   | 15016,11066 |
| 10620,14869   | 10620,14869 |
| 13891,12892   | 13891,12892 |
| 12264,10397   | 12264,10397 |
| 11066,12892   | 11066,12892 |
