---
description: >-
  This section contains reference documentation for the arraySortInt
  function.
---

# arraySortInt

Sorts array of ints.

## Signature

> arraySortInt('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arraySortInt(DivAirportIDs) AS sortedIds
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

| DivAirportIDs | sortedIds|
| --------- | -------- | 
|13891,12892|	12892,13891|
|14683,14683|	14683,14683|
|12339,12339|	12339,12339|
|13198,10721|	10721,13198|
|10721,12478|	10721,12478|