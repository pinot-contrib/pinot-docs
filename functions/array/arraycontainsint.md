---
description: >-
  This section contains reference documentation for the arrayContainsInt
  function.
---

# arrayContainsInt

Checks if int value exists in array.

## Signature

> arrayContainsInt('colName', valueToFind)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select DivAirportIDs, 
       arrayContainsInt(DivAirportIDs, 14683) AS containsValue
from airlineStats 
WHERE arraylength(DivAirportIDs) >= 2
limit 5
```

| DivAirportIDs | containsValue |
| ------------- | ------------- |
| 13891,12892   | false         |
| 14683,14683   | true          |
| 12339,12339   | false         |
| 13487,13930   | false         |
| 13029,11292   | false         |
