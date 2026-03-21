---
description: This section contains reference documentation for the MULT function.
---

# mult

Product of at least two values

## Signature

> MULT(col1, col2, col3...)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select homeRuns, baseOnBalls, MULT(homeRuns, baseOnBalls) AS total
from baseballStats 
WHERE teamID = 'ML1' 
AND yearID = 1956 
AND playerName = 'Henry Louis'
```

| homeRuns | baseOnBalls | total |
| -------- | ----------- | ----- |
| 26       | 37          | 962   |
