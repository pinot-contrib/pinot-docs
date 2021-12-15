---
description: This section contains reference documentation for the week function.
---

# week

Returns the ISO week of the year from the given epoch millis in UTC or specified timezone. 
The value ranges from 1 to 53. 

## Signature

> week(tsInMillis)
>
> week(tsInMillis, timeZoneId)
>
> weekOfYear(tsInMillis)
>
> weekOfYear(tsInMillis, timeZoneId)

## Usage Examples

```sql
select week(1639351800000) AS week
FROM ignoreMe
```

| week   |
| ------------- |
| 49 |

```sql
select week(1639351800000, 'CET') AS week
FROM ignoreMe
```

| week   |
| ------------- |
| 50 |

```sql
select weekOfYear(1639351800000) AS week
FROM ignoreMe
```

| week   |
| ------------- |
| 49 |

```sql
select weekOfYear(1639351800000, 'CET') AS week
FROM ignoreMe
```

| week   |
| ------------- |
| 50 |