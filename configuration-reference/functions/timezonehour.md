---
description: This section contains reference documentation for the timezoneHour function.
---

# timezoneHour

Returns the hour of the time zone offset. The timezoneId provided should be in [Joda Time format](https://www.joda.org/joda-time/timezones.html).

## Signature

> timezoneHour(timezoneId)

## Usage Examples

```sql
SELECT timezoneHour('America/Toronto') AS hour
FROM ignoreMe
```

| hour |
| ---- |
| 19   |

```sql
SELECT timezoneHour('UTC') AS hour
FROM ignoreMe
```

| hour |
| ---- |
| 0    |

```sql
SELECT timezoneHour('Europe/Rome') AS hour
FROM ignoreMe
```

| hour |
| ---- |
| 1    |
