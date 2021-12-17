---
description: This section contains reference documentation for the SEGMENTPARTITIONEDDISTINCTCOUNT function.
---

# SEGMENTPARTITIONEDDISTINCTCOUNT

Returns the count of distinct values of a column when the column is pre-partitioned for each segment, where there is no common value within different segments. 
This function calculates the exact count of distinct values within the segment, then simply sums up the results from different segments to get the final result. 

{% hint style="warning" %}
This function relies on the expression values being partitioned for each segment, where there are no common values within different segments.
{% endhint %}


## Signature

> SEGMENTPARTITIONEDDISTINCTCOUNT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select SEGMENTPARTITIONEDDISTINCTCOUNT(teamID) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 149 |
