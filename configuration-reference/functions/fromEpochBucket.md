---
description: This section contains reference documentation for the fromEpochBucket functions.
---

# fromEpochBucket

Convert epoch <Bucket Size><Time Unit> to epoch milliseconds. e.g. 10 seconds since epoch or 5 minutes since Epoch. 
The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> ToEpoch<TIME_UNIT>Bucket(timeInMillis, bucketSize)

## Usage Examples

```sql
select FromEpochSecondsBucket(1613472303, 1) AS bucket
FROM ignoreMe
```

| bucket   |
| ------------- |
| 1613472303000 |

```sql
select FromEpochSecondsBucket(1613472303, 2) AS bucket
FROM ignoreMe
```

| bucket   |
| ------------- |
| 3226944606000 |

```sql
select FromEpochMinutesBucket(2689120, 10) AS bucket
FROM ignoreMe
```

| bucket   |
| ------------- |
| 1613472000000 |

```sql
select FromEpochHoursBucket(89637, 5) AS bucket
FROM ignoreMe
```

| bucket   |
| ------------- |
| 1613466000000 |

```sql
select FromEpochDaysBucket(1867, 10) AS bucket
FROM ignoreMe
```

| bucket   |
| ------------- |
| 1613088000000 |


