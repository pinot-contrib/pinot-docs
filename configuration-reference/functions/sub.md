---
description: This section contains reference documentation for the SUB function.
---

# SUB

Difference between two values

## Signature

> SUB(col1, col2)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select homeRuns, baseOnBalls, SUB(homeRuns, baseOnBalls) AS total
from baseballStats 
WHERE teamID = 'ML1' 
AND yearID = 1956 
AND playerName = 'Henry Louis'
```

| homeRuns   | baseOnBalls | total | 
| ------------- | ------------- | ------------- | 
| 26 | 37  | 	-11 | 
