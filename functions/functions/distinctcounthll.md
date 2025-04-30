---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLL
  function.
---

# DISTINCTCOUNTHLL

Returns an approximate distinct count using _HyperLogLog_. It also takes an optional second argument to configure the _log2m_ for the _HyperLogLog_.&#x20;

For accurate distinct counting, see [DISTINCTCOUNT](distinctcount.md). Review [DISTINCTCOUNTHLL considerations](distinctcounthll.md#distinctcounthll-considerations) for your use case.

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

## **DISTINCTCOUNTHLL considerations**

* `DISTINCTCOUNTHLL()`is faster than `DISTINCTCOUNT()`if data is pre-aggregated at ingestion or aggregated at a server with enough records. This performance improvement increases when comparing large datasets.
* If very few records are pre-aggregated, `DISTINCTCOUNTHLL()`will not be as fast as `DISTINCTCOUNT()`because the serialized HLL size is larger than sending individual values.
* `DISTINCTCOUNTHLLPLUS()`provides more precise results than `DISTINCTCOUNTHLL()`with the same performance.
* `DISTINCTCOUNTSMARTHLL()`automatically shifts to HLL when reaching a threshold, and comes with some overhead.

