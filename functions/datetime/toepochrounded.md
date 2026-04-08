---
description: >-
  This section contains reference documentation for the toEpochRounded
  functions.
---

# ToEpochRounded

Convert epoch milliseconds to epoch , round to nearest rounding bucket(Bucket size is defined in ) The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> ToEpoch\<TIME\_UNIT>Rounded(timeInMillis, bucketSize)

## Usage Examples

```sql
select ToEpochSecondsRounded(1613472303000, 1000) AS epochSeconds
FROM ignoreMe
```

| epochSeconds |
| ------------ |
| 1613472000   |

```sql
select ToEpochMinutesRounded(1613472303000, 10) AS epochMins
FROM ignoreMe
```

| epochMins |
| --------- |
| 26891200  |

```sql
select ToEpochHoursRounded(1613472303000, 5) AS epochHours
FROM ignoreMe
```

| epochHours |
| ---------- |
| 448185     |

```sql
select ToEpochDaysRounded(1613472303000, 10) AS epochDays
FROM ignoreMe
```

| epochDays |
| --------- |
| 18670     |
