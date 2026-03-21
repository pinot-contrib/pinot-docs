---
description: >-
  This section contains reference documentation for the arraySliceString
  function.
---

# arraySliceString

Returns the values in the array between the start and end positions.

## Signature

> arraySliceString('colName', start, end)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arraySliceString(RandomAirports, 0, 2) AS airports, 
       RandomAirports
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

| FlightNum | airports | RandomAirports  |
| --------- | -------- | --------------- |
| 671       | SEA,PSC  | SEA,PSC,PHX,MSY |
| 1767      | SEA,PSC  | SEA,PSC,PHX     |
| 2522      | SEA,PSC  | SEA,PSC         |
| 424       | SEA,PSC  | SEA,PSC,PHX,MSY |
| 3162      | SEA,PSC  | SEA,PSC,PHX,MSY |
