---
description: This section contains reference documentation for the year function.
---

# year

Returns the year from the given epoch millis in UTC timezone.

## Signature

> year(tsInMillis)
>
> year(tsInMillis, timeZoneId)

## Usage Examples

```sql
select year(1609472186000) AS year
FROM ignoreMe
```

| year |
| ---- |
| 2021 |

```sql
select year(1609472186000, 'America/Toronto') AS year
FROM ignoreMe
```

| year |
| ---- |
| 2020 |
