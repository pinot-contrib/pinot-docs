---
description: This section contains reference documentation for the day function.
---

# day

Returns the day of the month from the given epoch millis in UTC or specified timezone. The value ranges from 1 to 31.

## Signature

> day(tsInMillis)
>
> day(tsInMillis, timeZoneId)
>
> dayOfMonth(tsInMillis)
>
> dayOfMonth(tsInMillis, timeZoneId)

## Usage Examples

```sql
select day(1639351800000) AS day
FROM ignoreMe
```

| day |
| --- |
| 12  |

```sql
select day(1639351800000, 'CET') AS day
FROM ignoreMe
```

| day |
| --- |
| 13  |

```sql
select dayOfMonth(1639351800000) AS day
FROM ignoreMe
```

| day |
| --- |
| 12  |

```sql
select dayOfMonth(1639351800000, 'CET') AS day
FROM ignoreMe
```

| day |
| --- |
| 13  |
