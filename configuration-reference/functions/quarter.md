---
description: This section contains reference documentation for the quarter function.
---

# quarter

Returns the quarter of the year from the given epoch millis in UTC or specified timezone. 
The value ranges from 1 to 4

## Signature

> quarter(tsInMillis)
>
> quarter(tsInMillis, timeZoneId)

## Usage Examples

```sql
select quarter(1633046399000) AS quarter
FROM ignoreMe
```

| quarter   |
| ------------- |
| 3 |

```sql
select quarter(1633046399000, 'UTC') AS quarter
FROM ignoreMe
```

| quarter   |
| ------------- |
| 3 |

```sql
select quarter(1633046399000, 'CET') AS quarter
FROM ignoreMe
```

| quarter   |
| ------------- |
| 4 |

