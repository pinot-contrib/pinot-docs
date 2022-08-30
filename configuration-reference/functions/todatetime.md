---
description: This section contains reference documentation for the ToDateTime function.
---

# ToDateTime

Converts from milliseconds to a formatted date-time string, based on the provided [Joda-Time pattern](https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html).

## Signature

> ToDate(millis, pattern)&#x20;
>
> ToDate(millis, pattern, timezoneId)

## Usage Examples

```sql
SELECT ToDateTime(1639137263000, 'yyyy-MM-dd') AS dateTimeString
FROM ignoreMe
```

| dateTimeString |
| -------------- |
| 2021-12-10     |

```sql
SELECT ToDateTime(
    1639137263000, 
    'yyyy-MM-dd hh:mm:ss a'
    ) AS dateTimeString
FROM ignoreMe
```

| dateTimeString         |
| ---------------------- |
| 2021-12-10 11:54:23 AM |

```sql
SELECT ToDateTime(
    1639137263000, 
    'yyyy-MM-dd HH:mm:ss Z',
    'CET'
    ) AS dateTimeString
FROM ignoreMe
```

| dateTimeString            |
| ------------------------- |
| 2021-12-10 12:54:23 +0100 |
