---
description: This section contains reference documentation for the DISTINCTCOUNT function.
---

# DISTINCTCOUNT


Returns the count of distinct row values in a group

## Signature

> DISTINCTCOUNT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCTCOUNT(league) AS value
from baseballStats 
```

| value   | 
| ------------- |
|7 |

```sql
select DISTINCTCOUNT(teamID) AS value
from baseballStats 
```

| value   | 
| ------------- |
| 149 |