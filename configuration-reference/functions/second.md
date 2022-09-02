---
description: This section contains reference documentation for the second function.
---

# second

Returns the second of the minute from the given epoch millis in UTC or specified timezone. The value ranges from 0 to 59.

## Signature

> second(tsInMillis)
>
> second(tsInMillis, timeZoneId)

## Usage Examples

```sql
select second(1639351800000) AS second
FROM ignoreMe
```

| second |
| ------ |
| 0      |

```sql
select second(1639351800000, 'America/St_Johns') AS second
FROM ignoreMe
```

| second |
| ------ |
| 0      |
