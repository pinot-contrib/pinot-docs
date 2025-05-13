---
description: This section contains reference documentation for the yearOfWeek function.
---

# yearOfWeek

Returns the year of the ISO week from the given epoch millis and timezone id. Alias `yow`is also supported.

## Signature

> yearOfWeek(tsInMillis)
>
> yearOfWeek(tsInMillis, timeZoneId)

> yow(tsInMillis)
>
> yow(tsInMillis, timeZoneId)

## Usage Examples

```sql
select yearOfWeek(1609731386000) AS year
FROM ignoreMe
```

| year |
| ---- |
| 2021 |

```sql
select yearOfWeek(1609731386000, 'America/Toronto') AS year
FROM ignoreMe
```

| year |
| ---- |
| 2020 |

```sql
select yow(1609731386000) AS year
FROM ignoreMe
```

| year |
| ---- |
| 2021 |

```sql
select yow(1609731386000, 'America/Toronto') AS year
FROM ignoreMe
```

| year |
| ---- |
| 2020 |
