---
description: This section contains reference documentation for the month function.
---

# month

Returns the month of the year from the given epoch millis in UTC or specified timezone. The value ranges from 1 to 12.

## Signature

> month(tsInMillis)
>
> month(tsInMillis, timeZoneId)

## Usage Examples

```sql
select month(1633046399000, 'UTC') AS month
FROM ignoreMe
```

| month |
| ----- |
| 9     |

```sql
select month(1633046399000, 'CET') AS month
FROM ignoreMe
```

| month |
| ----- |
| 10    |
