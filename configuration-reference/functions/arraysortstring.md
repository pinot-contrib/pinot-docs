---
description: >-
  This section contains reference documentation for the arraySortString
  function.
---

# arraySortString

Sorts array of strings.

## Signature

> arraySortString('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select FlightNum, 
       arraySortString(RandomAirports) AS sortedAirports, 
       RandomAirports
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

| FlightNum | sortedAirports | RandomAirports  |
| --------- | -------- | --------------- |
|3846|	PSC,SEA	|SEA,PSC|
|3635|	MSY,PHX,PSC,SEA	|SEA,PSC,PHX,MSY|
|429|	MSY,PHX,PSC,SEA	|SEA,PSC,PHX,MSY|
|1206	|PSC,SEA	|SEA,PSC|
|5300|	PSC,SEA|	SEA,PSC|
