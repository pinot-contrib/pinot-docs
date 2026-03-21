---
description: >-
  This section contains reference documentation for the arrayRemoveString
  function.
---

# arrayRemoveString

Removes value from array of strings.

## Signature

> arrayRemoveString('colName', value)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select RandomAirports, 
       arrayRemoveString(RandomAirports, 'SEA') AS value
from airlineStats 
WHERE arraylength(RandomAirports) BETWEEN 2 AND 4
limit 5
```

| DivAirportIDs   | value       |
| --------------- | ----------- |
| SEA,PSC         | PSC         |
| SEA,PSC,PHX,MSY | PSC,PHX,MSY |
| SEA,PSC,PHX,MSY | PSC,PHX,MSY |
| SEA,PSC         | PSC         |
| SEA,PSC         | PSC         |
