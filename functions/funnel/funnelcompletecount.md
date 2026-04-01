---
description: This section contains reference documentation for the FUNNELCOMPLETECOUNT function.
---

# FUNNELCOMPLETECOUNT

Returns the count of entities that completed all steps in a funnel. This function is part of the funnel analysis family and counts only those entities (identified by the correlation column) that progressed through every defined funnel step.

## Signature

> FUNNELCOMPLETECOUNT(stepColumn, correlationColumn, settings, step1, step2, ...)

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
      <td>`settings`</td>
      <td>Configuration string for funnel behavior</td>
    </tr>
    <tr>
      <td>`step1, step2, ...`</td>
      <td>Boolean expressions defining each funnel step</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>completedCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1250</td>
    </tr>
  </tbody>
</table>

For more information on funnel analysis, see [Funnel Count](funnelcount.md) and [Funnel Max Step](funnelmaxstep.md).
