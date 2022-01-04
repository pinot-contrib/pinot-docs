---
description: This section contains reference documentation for the percentile function.
---

# percentile

Returns the `max` - `min` value in a group

## Signature

> percentile(colName, percentile)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select percentile(homeRuns, 50) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 0 | 

```sql
select percentile(homeRuns, 80) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 4 | 

```sql
select percentile(homeRuns, 99.9) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 46 | 