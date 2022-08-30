---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLL
  function.
---

# DISTINCTCOUNTHLL

Returns an approximate distinct count using _HyperLogLog_. It also takes an optional second argument to configure the _log2m_ for the _HyperLogLog_.\
For accurate distinct counting, see [DISTINCTCOUNT](distinctcount.md).

## Signature

> DISTINCTCOUNTHLL(colName, log2m)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCTCOUNTHLL(teamID) AS value
from baseballStats 
```

| value |
| ----- |
| 158   |

```sql
select DISTINCTCOUNTHLL(teamID, 12) AS value
from baseballStats 
```

| value |
| ----- |
| 149   |
