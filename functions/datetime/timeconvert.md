---
description: This section contains reference documentation for the TIMECONVERT function.
---

# TIMECONVERT

Converts the value from a column that contains an epoch timestamp into another time unit. The converted value will be rounded down.

## Signature

> TIMECONVERT(col, fromUnit, toUnit)

The supported units are as follows:

* DAYS
* HOURS
* MINUTES
* SECONDS
* MILLISECONDS
* MICROSECONDS
* NANOSECONDS

## Usage Examples

These examples are based on the [Batch JSON Quick Start](../../basics/getting-started/quick-start.md#batch-json).

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'DAYS') AS convertedTime
from githubEvents
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>created\_at\_timestamp</th>
      <th>timeInMs</th>
      <th>convertedTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>2018-01-01 11:00:00.0</td>
      <td>1514804400000</td>
      <td>17532</td>
    </tr>
  </tbody>
</table>

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'HOURS') AS convertedTime
from githubEvents
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>created\_at\_timestamp</th>
      <th>timeInMs</th>
      <th>convertedTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>2018-01-01 11:00:00.0</td>
      <td>1514804400000</td>
      <td>420779</td>
    </tr>
  </tbody>
</table>

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'SECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>created\_at\_timestamp</th>
      <th>timeInMs</th>
      <th>convertedTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>2018-01-01 11:00:00.0</td>
      <td>1514804400000</td>
      <td>1514804400</td>
    </tr>
  </tbody>
</table>

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'MILLISECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>created\_at\_timestamp</th>
      <th>timeInMs</th>
      <th>convertedTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>2018-01-01 11:00:00.0</td>
      <td>1514804400000</td>
      <td>1514804400000</td>
    </tr>
  </tbody>
</table>

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'MICROSECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>created\_at\_timestamp</th>
      <th>timeInMs</th>
      <th>convertedTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>2018-01-01 11:00:00.0</td>
      <td>1514804400000</td>
      <td>1514804400000000</td>
    </tr>
  </tbody>
</table>

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'NANOSECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>created\_at\_timestamp</th>
      <th>timeInMs</th>
      <th>convertedTime</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7044874109</td>
      <td>2018-01-01 11:00:00.0</td>
      <td>1514804400000</td>
      <td>1514804400000000000</td>
    </tr>
  </tbody>
</table>
