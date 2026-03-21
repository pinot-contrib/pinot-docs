---
description: This section contains reference documentation for the FUNNELSTEPDURATIONSTATS function.
---

# FUNNELSTEPDURATIONSTATS

Calculates duration statistics between funnel steps. Returns an array of computed statistics (such as average, median, min, max, count, or percentiles) for the time elapsed between consecutive funnel steps. This function is part of the funnel analysis family and requires a windowed funnel configuration.

## Signature

> FUNNELSTEPDURATIONSTATS(stepColumn, correlationColumn, timestampColumn, 'settings', step1, step2, ...)

Parameters:

| Parameter | Description |
| --------- | ----------- |
| `stepColumn` | Column used to identify which step an event belongs to |
| `correlationColumn` | Column used to correlate events from the same entity (e.g., user ID) |
| `timestampColumn` | Column containing the event timestamp |
| `settings` | Configuration string including `DURATIONFUNCTIONS` (comma-separated: AVG, MEDIAN, MIN, MAX, COUNT, PERCENTILEx) |
| `step1, step2, ...` | Boolean expressions defining each funnel step |

## Usage Examples

```sql
select FUNNELSTEPDURATIONSTATS(
  stepCol,
  visitorId,
  ts,
  'DURATIONFUNCTIONS(AVG,MEDIAN,MAX)',
  url = '/home',
  url = '/product',
  url = '/checkout'
) AS durationStats
from eventTable
```

| durationStats              |
| -------------------------- |
| [120.5, 100.0, 350.0, ...] |

For more information on funnel analysis, see [Funnel Functions](../funnel/).
