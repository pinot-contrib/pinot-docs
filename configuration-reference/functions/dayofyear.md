---
description: This section contains reference documentation for the dayOfYear function.
---

# dayOfYear

Returns the day of the year from the given epoch millis in UTC or specified timezone. 
The value ranges from 1 to 366.

## Signature

> dayOfYear(tsInMillis)
>
> dayOfYear(tsInMillis, timeZoneId)
>
> doy(tsInMillis)
>
> doy(tsInMillis, timeZoneId)

## Usage Examples

```sql
select dayOfYear(1639351800000) AS dayOfYear
FROM ignoreMe
```

| dayOfYear   |
| ------------- |
| 346 |

```sql
select dayOfYear(1639351800000, 'CET') AS dayOfYear
FROM ignoreMe
```

| dayOfYear   |
| ------------- |
| 347 |

```sql
select doy(1639351800000) AS dayOfYear
FROM ignoreMe
```

| dayOfYear   |
| ------------- |
| 346 |

```sql
select doy(1639351800000, 'CET') AS dayOfYear
FROM ignoreMe
```

| dayOfYear   |
| ------------- |
| 347 |
