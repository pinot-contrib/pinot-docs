---
description: This section contains reference documentation for the DIV function.
---

# DIV

Quotient of two values

## Signature

> DIV(col1, col2)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select homeRuns, numberOfGames, DIV(homeRuns, numberOfGames) AS total
from baseballStats 
WHERE teamID = 'ML1' 
AND yearID = 1956 
AND playerName = 'Henry Louis'
```

| homeRuns | numberOfGames | total               |
| -------- | ------------- | ------------------- |
| 26       | 153           | 0.16993464052287582 |
