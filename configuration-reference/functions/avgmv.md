---
description: This section contains reference documentation for the AVGMV function.
---

# AVGMV

Get the avg of values in a group


## Signature

> AVGMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select AVGMV(DivLongestGTimes) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

| value   | 
| ------------- |
| 18.465753424657535 | 
