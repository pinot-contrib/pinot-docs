---
description: This section contains reference documentation for the PERCENTILEMV function.
---

# percentilemv

Returns the Nth percentile of the group where N is a decimal number between 0 and 100 inclusive

## Signature

> PERCENTILEMV(colName, N)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select PERCENTILEMV(DivLongestGTimes, 50) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>10</td>
    </tr>
  </tbody>
</table>

```sql
select PERCENTILEMV(DivLongestGTimes, 90) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>44</td>
    </tr>
  </tbody>
</table>

```sql
select PERCENTILEMV(DivLongestGTimes, 99.9) AS value
from airlineStats 
where arraylength(DivLongestGTimes) > 1
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>108</td>
    </tr>
  </tbody>
</table>
