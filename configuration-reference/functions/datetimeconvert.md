---
description: >-
  This section contains reference documentation for the DATETIMECONVERT
  function.
---

# DATETIMECONVERT

Converts the value from a column that contains an epoch timestamp into another time unit and buckets based on the given time granularity.

## Signature

> DATETIMECONVERT(columnName, inputFormat, outputFormat, outputGranularity)

`inputFormat` and `outputFormat` are defined using the following structure:

`<time size>:<time unit>:<time format>:<pattern>`

where:

* `time size` - size of the time unit eg: 1, 10
* `time unit` - `DAYS`, `HOURS`, `MINUTES`, `SECONDS`, `MILLISECONDS`, `MICROSECONDS`, `NANOSECONDS`
* `time format`
  * `EPOCH`&#x20;
  * `SIMPLE_DATE_FORMAT` pattern - defined in case of `SIMPLE_DATE_FORMAT` e.g. `yyyy-MM-dd`. A specific timezone can be passed using `tz(timezone)`. Timezone can be long or short string format timezone. e.g. `Asia/Kolkata` or `PDT`

`granularity` is specified in the format `<time size>:<time unit>`.

## Usage Examples

These examples are based on the [Batch JSON Quick Start](../../basics/getting-started/quick-start.md#batch-json).

`created_at_timestamp` from milliseconds since epoch to days since epoch, bucketed to 1 day granularity:

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       DATETIMECONVERT(
         created_at_timestamp, 
         '1:MILLISECONDS:EPOCH', 
         '1:DAYS:EPOCH', 
         '1:DAYS'
       ) AS convertedTime
from githubEvents
WHERE id = 7044874134
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874134 | 2018-01-01 11:00:00.0  | 1514804402000 | 17532         |

`created_at_timestamp` bucketed to 15 minutes granularity:

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       DATETIMECONVERT(
         created_at_timestamp, 
         '1:MILLISECONDS:EPOCH', 
         '1:MILLISECONDS:EPOCH', 
         '15:MINUTES'
       ) AS convertedTime
from githubEvents
WHERE id = 7044874134
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874134 | 2018-01-01 11:00:00.0  | 1514804402000 | 1514804400000 |

`created_at_timestamp` to format `yyyy-MM-dd`, bucketed to 1 days granularity:

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       DATETIMECONVERT(
         created_at_timestamp, 
         '1:MILLISECONDS:EPOCH', 
         '1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd', 
         '1:DAYS'
       ) AS convertedTime
from githubEvents
WHERE id = 7044874134
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874134 | 2018-01-01 11:00:00.0  | 1514804402000 | 2018-01-01    |

`created_at_timestamp` to format `yyyy-MM-dd HH:mm`, in timezone `Pacific/Kiritimati`:

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       DATETIMECONVERT(
         created_at_timestamp, 
         '1:MILLISECONDS:EPOCH', 
         '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm tz(Pacific/Kiritimati)', 
         '1:MILLISECONDS'
       ) AS convertedTime
from githubEvents
WHERE id = 7044874134
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime    |
| ---------- | ---------------------- | ------------- | ---------------- |
| 7044874134 | 2018-01-01 11:00:00.0  | 1514804402000 | 2018-01-02 01:00 |

`created_at_timestamp` to format `yyyy-MM-dd`, in timezone `Pacific/Kiritimati` and bucketed to 1 day granularity:

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       DATETIMECONVERT(
         created_at_timestamp, 
         '1:MILLISECONDS:EPOCH', 
         '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm tz(Pacific/Kiritimati)', 
         '1:DAYS'
       ) AS convertedTime
from githubEvents
WHERE id = 7044874134
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime    |
| ---------- | ---------------------- | ------------- | ---------------- |
| 7044874134 | 2018-01-01 11:00:00.0  | 1514804402000 | 2018-01-02 00:00 |
