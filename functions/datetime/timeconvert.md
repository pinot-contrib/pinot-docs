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

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874109 | 2018-01-01 11:00:00.0  | 1514804400000 | 17532         |

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'HOURS') AS convertedTime
from githubEvents
LIMIT 1
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874109 | 2018-01-01 11:00:00.0  | 1514804400000 | 420779        |

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'SECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874109 | 2018-01-01 11:00:00.0  | 1514804400000 | 1514804400    |

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'MILLISECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime |
| ---------- | ---------------------- | ------------- | ------------- |
| 7044874109 | 2018-01-01 11:00:00.0  | 1514804400000 | 1514804400000 |

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'MICROSECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime    |
| ---------- | ---------------------- | ------------- | ---------------- |
| 7044874109 | 2018-01-01 11:00:00.0  | 1514804400000 | 1514804400000000 |

```sql
select id, 
       created_at_timestamp, 
       cast(created_at_timestamp AS long) AS timeInMs,
       TIMECONVERT(created_at_timestamp, 'MILLISECONDS', 'NANOSECONDS') AS convertedTime
from githubEvents
LIMIT 1
```

| id         | created\_at\_timestamp | timeInMs      | convertedTime       |
| ---------- | ---------------------- | ------------- | ------------------- |
| 7044874109 | 2018-01-01 11:00:00.0  | 1514804400000 | 1514804400000000000 |
