---
description: >-
  This section contains reference documentation for the DATETRUNC function.
---

# DATETRUNC

(Presto) SQL compatible date truncation, equivalent to the Presto function `date_trunc`.

Converts the value into a specified output granularity seconds since UTC epoch that is bucketed on a unit in a specified timezone.

## Signature

> DATETRUNC(unit, timeValue) 
>
> DATETRUNC(unit, timeValue, inputTimeUnitStr) 
>
> DATETRUNC(unit, timeValue, inputTimeUnitStr, timeZone) 
>
> DATETRUNC(unit, timeValue, inputTimeUnitStr, timeZone, outputTimeUnitStr) 

`unit` supports the following values:

* millisecond
* second
* minute
* hour
* day
* week
* month
* quarter
* year

`inputTimeUnitStr` and `outputTimeUnitStr` support the following values:

* NANOSECONDS
* MICROSECONDS
* MILLISECONDS
* SECONDS
* MINUTES 
* HOURS
* DAYS

## Usage Examples

Truncates an epoch in milliseconds at `WEEK` (where a Week starts at Monday UTC midnight):

```sql
select dateTrunc('week', 1639480981746) AS ts
FROM ignoreMe
```

or

```sql
select dateTrunc('week', 1639480981746, 'MILLISECONDS') AS ts
FROM ignoreMe
```

| ts         |
| ---------- |
| 1639353600000 |


Truncates an epoch in milliseconds at `WEEK` (where a Week starts at Monday UTC midnight) in the `UTC` time zone, returning a result in epoch in seconds in UTC timezone:

```sql
select dateTrunc('week', 1639480981746, 'MILLISECONDS', 'UTC', 'SECONDS') AS ts
FROM ignoreMe
```

| ts         |
| ---------- |
| 1639353600 |

Truncates an epoch in milliseconds at `WEEK` (where a Week starts at Monday UTC midnight) in the `CET` time zone, returning a result in epoch in seconds in UTC timezone:

```sql
select dateTrunc('week', 1639480981746, 'MILLISECONDS', 'CET', 'SECONDS') AS ts
FROM ignoreMe
```

| ts         |
| ---------- |
| 1639350000 |


Truncates an epoch in milliseconds at `QUARTER` in the Los Angeles time zone (where a Quarter begins on Na 1st, April 1st, July 1st, October 1st in Los Angeles timezone), returning a result in hours since UTC epoch:

```sql
select dateTrunc('quarter', 1639480981746, 'MILLISECONDS', 'America/Los_Angeles', 'HOURS') AS ts
FROM ignoreMe
```

| ts         |
| ---------- |
| 453631 |