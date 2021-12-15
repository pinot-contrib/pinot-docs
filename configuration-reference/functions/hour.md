---
description: This section contains reference documentation for the hour function.
---

# hour

Returns the hour of the day from the given epoch millis in UTC or specified timezone. 
The value ranges from 0 to 23.

## Signature

> hour(tsInMillis)
>
> hour(tsInMillis, timeZoneId)

## Usage Examples

```sql
select hour(1639351800000) AS hour
FROM ignoreMe
```

| hour   |
| ------------- |
| 23 |

```sql
select hour(1639351800000, 'CET') AS hour
FROM ignoreMe
```

| hour   |
| ------------- |
| 0 |