---
description: >-
  This section contains reference documentation for the PERCENTILERAWKLLMV function.
---

# PERCENTILRAWEKLLMV

Variant of the `PERCENTILERAWKLL` aggregation function which accepts multi-value columns. Values in the given column are 'flattened' before aggregation.

## Signature

> PercentileRAWKLLMV(column, percentile) -> Double

* `column` (required): Name of the column to aggregate on. 
* `percentile` (required): Percentile value to be calculated [0..100]. For raw versions of the function, this value is used for ordering (ORDER BY).

## Usage Examples

```sql
select percentileKLLMV(ArrOfInts, 90) as value
from MyTable
```

| sketch   |
| -------- |
| BQEPC... |
