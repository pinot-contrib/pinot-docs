---
description: This section contains reference documentation for the HISTOGRAM function.
---

# HISTOGRAM


Returns the count of data points that fall within each bin as a vector.
The bins are left-inclusive and right-exclusive, i.e. `[a, b)`, except for the last one 
which is inclusive on both sides `[a, b]`.

## Signatures
1. Equal length bins (better performance):
> HISTOGRAM(colName, lower, upper, numBins)

2. Arbitrary increasing bin edges:
> HISTOGRAM(colName, ARRAY[binEdge1, binEdge2, binEdge3, ...]) 

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

1. 10 equal-length bins `[0, 20), [20, 30) ... [180, 200]`
```sql
SELECT HISTOGRAM(numberOfGames, 0, 200, 10) AS histogram
FROM baseballStats 
```

| histogram   | 
| ------------- |
|32348,21519,11359,7587,5488,5360,6282,7361,585,0 |

2. 6 bins `(- ∞, 1), [1, 10), [10, 50), [50,100), [100,500), [500, 1000]`

```sql
select HISTOGRAM(AtBatting, Array['-Infinity', 1, 10, 50, 100, 500, 1000]) AS histogram
from baseballStats

```

| histogram   | 
| ------------- |
| 13520,16506,18375,12403,28591,8494 |