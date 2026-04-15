---
description: This section contains reference documentation for the DISTINCTCOUNT function.
---

# DISTINCTCOUNT

Returns the count of distinct row values in a group.

{% hint style="info" %}
`DISTINCTCOUNTHLL()`is faster than `DISTINCTCOUNT()`if data is pre-aggregated at ingestion or aggregated at a server with enough records. This performance improvement increases when comparing large datasets.

If very few records are pre-aggregated, `DISTINCTCOUNT()`is faster than `DISTINCTCOUNTHLL()`because the serialized HLL size is larger than sending individual values.
{% endhint %}

## Signature

> DISTINCTCOUNT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select DISTINCTCOUNT(league) AS value
from baseballStats 
```

| value |
| ----- |
| 7     |

```sql
select DISTINCTCOUNT(teamID) AS value
from baseballStats 
```

| value |
| ----- |
| 149   |
