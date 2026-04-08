---
description: This section contains reference documentation for the millisecond function.
---

# millisecond

Returns the millisecond of the second from the given epoch millis in UTC or specified timezone. The value ranges from 0 to 999.

## Signature

> millisecond(tsInMillis)
>
> millisecond(tsInMillis, timeZoneId)

## Usage Examples

```sql
select millisecond(1639351800000) AS millisecond
FROM ignoreMe
```

| millisecond |
| ----------- |
| 0           |

```sql
select millisecond(1639351800000, 'America/St_Johns') AS millisecond
FROM ignoreMe
```

| millisecond |
| ----------- |
| 0           |
