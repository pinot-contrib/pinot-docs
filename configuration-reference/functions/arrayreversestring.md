---
description: >-
  This section contains reference documentation for the arrayReverseString
  function.
---

# arrayReverseString

Reverses array of strings.

## Signature

> arrayReverseString('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arrayReverseString(RandomAirports) AS reversedAirports, 
       RandomAirports
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

| FlightNum | reversedAirports | RandomAirports  |
| --------- | ---------------- | --------------- |
| 1206      | PSC,SEA          | SEA,PSC         |
| 5300      | PSC,SEA          | SEA,PSC         |
| 3359      | MSY,PHX,PSC,SEA  | SEA,PSC,PHX,MSY |
| 1023      | PHX,PSC,SEA      | SEA,PSC,PHX     |
| 963       | MSY,PHX,PSC,SEA  | SEA,PSC,PHX,MSY |
