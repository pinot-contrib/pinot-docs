---
description: This section contains reference documentation for the FUNNELSTEPDURATIONSTATS function.
---

# FUNNELSTEPDURATIONSTATS

Calculates duration statistics between funnel steps. Returns an array of computed statistics (such as average, median, min, max, count, or percentiles) for the time elapsed between consecutive funnel steps. This function is part of the funnel analysis family and requires a windowed funnel configuration.

## Signature

> FUNNELSTEPDURATIONSTATS(stepColumn, correlationColumn, timestampColumn, 'settings', step1, step2, ...)

Parameters:

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`stepColumn`</td>
      <td>Column used to identify which step an event belongs to</td>
    </tr>
    <tr>
      <td>`correlationColumn`</td>
      <td>Column used to correlate events from the same entity (e.g., user ID)</td>
    </tr>
    <tr>
      <td>`timestampColumn`</td>
      <td>Column containing the event timestamp</td>
    </tr>
    <tr>
      <td>`settings`</td>
      <td>Configuration string including `DURATIONFUNCTIONS` (comma-separated: AVG, MEDIAN, MIN, MAX, COUNT, PERCENTILEx)</td>
    </tr>
    <tr>
      <td>`step1, step2, ...`</td>
      <td>Boolean expressions defining each funnel step</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>durationStats</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[120.5, 100.0, 350.0, ...]</td>
    </tr>
  </tbody>
</table>

For more information on funnel analysis, see [Funnel Functions](../funnel/).
