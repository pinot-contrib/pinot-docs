---
description: This section contains reference documentation for the arrayReverseInt function.
---

# arrayReverseInt

Reverses array of ints.

## Signature

> arrayReverseInt('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select DivAirportIDs, 
       arrayReverseInt(DivAirportIDs) AS reversedIds
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

| DivAirportIDs	|reversedIds|
| ------------- | ------------- |
|13891,12892|	12892,13891|
|14683,14683|	14683,14683|
|12339,12339|	12339,12339|
|13487,13930|	13930,13487|
|13029,11292|	11292,13029|