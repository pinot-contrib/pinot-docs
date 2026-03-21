---
description: This section contains reference documentation for the FUNNELCOMPLETECOUNT function.
---

# FUNNELCOMPLETECOUNT

Returns the count of entities that completed all steps in a funnel. This function is part of the funnel analysis family and counts only those entities (identified by the correlation column) that progressed through every defined funnel step.

## Signature

> FUNNELCOMPLETECOUNT(stepColumn, correlationColumn, settings, step1, step2, ...)

Parameters:

| Parameter | Description |
| --------- | ----------- |
| `stepColumn` | Column used to identify which step an event belongs to |
| `correlationColumn` | Column used to correlate events from the same entity (e.g., user ID) |
| `settings` | Configuration string for funnel behavior |
| `step1, step2, ...` | Boolean expressions defining each funnel step |

## Usage Examples

```sql
select FUNNELCOMPLETECOUNT(
  stepCol,
  visitorId,
  '',
  url = '/home',
  url = '/product',
  url = '/checkout'
) AS completedCount
from eventTable
```

| completedCount |
| -------------- |
| 1250           |

For more information on funnel analysis, see [Funnel Count](funnelcount.md) and [Funnel Max Step](funnelmaxstep.md).
