---
description: >-
  This section contains reference documentation for the arrayIndexOfInt
  function.
---

# arrayIndexOfInt

Finds the last index of the given value in the array starting at the given index.

## Signature

> arrayIndexOfInt('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayIndexOfInt(DivAirportIDs, 14683) AS index
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

| DivAirportIDs | index |
| ------------- | ----- |
| 13891,12892   | -1    |
| 14683,14683   | 0     |
| 12339,12339   | -1    |
| 13487,13930   | -1    |
| 13029,11292   | -1    |
