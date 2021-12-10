---
description: >-
  This section contains reference documentation for the FromDateTime function.
---

# FromDateTime

Converts a formatted date time string to milliseconds, based on the provided [Joda-Time pattern](https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html). 

## Signature

> FromDateTime(dateTimeString, pattern)

## Usage Examples

```sql
SELECT FromDateTime('2019-08-07', 'YYYY-MM-dd') AS epochMillis
FROM ignoreMe
```

| epochMillis
| ----------- |
| 1565136000000|


```sql
SELECT FromDateTime('2019-08-07 3:12:13 PM', 'YYYY-MM-dd hh:mm:ss a') AS epochMillis
FROM ignoreMe
```

| epochMillis
| ----------- |
| 1565190733000|

```sql
SELECT FromDateTime('2019-08-07T15:12:13', 'YYYY-MM-dd''T''HH:mm:ss') AS epochMillis
FROM ignoreMe
```

| epochMillis
| ----------- |
| 1565190733000|


```sql
SELECT FromDateTime('2019-08-07T07:12:13-0800', 'YYYY-MM-dd''T''HH:mm:ssZ') AS epochMillis
FROM ignoreMe
```

| epochMillis
| ----------- |
| 1565190733000|

