---
description: This section contains reference documentation for the arraySliceInt function.
---

# arraySliceInt

Returns the values in the array between the start and end positions.

## Signature

> arraySliceInt('colName', start, end)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select FlightNum, 
       arraySliceInt(DivAirportIDs, 0, 1) AS airports, 
	     DivAirportIDs
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

| FlightNum   | airports | DivAirportIDs |
| ------------- | ------------- |------------- |
|1531	|13891|	13891,12892|
|19	|14683	|14683,14683|
|829|	12339	|12339,12339|
|24	|13198|13198,10721|
|548|	10721	|10721,12478|