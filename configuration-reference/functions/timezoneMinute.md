---
description: This section contains reference documentation for the timezoneMinute function.
---

# timezoneHour

Returns the minute of the time zone offset. The timezoneId provided should be in [Joda Time format](https://www.joda.org/joda-time/timezones.html).

## Signature

> timezoneMinute(timezoneId)

## Usage Examples

```sql
SELECT timezoneMinute('America/Toronto') AS minute
FROM ignoreMe
```

| hour   |
| ------------- |
| 0 |


```sql
SELECT timezoneMinute('Asia/Colombo') AS minute
FROM ignoreMe
```

| minute   |
| ------------- |
| 30 |


```sql
SELECT timezoneMinute('Asia/Kathmandu') AS minute
FROM ignoreMe
```

| minute   |
| ------------- |
| 45 |
