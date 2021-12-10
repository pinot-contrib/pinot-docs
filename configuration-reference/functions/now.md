---
description: This section contains reference documentation for the now function.
---

# now

Return current time as epoch millis.

## Signature

> now()


## Usage Examples

```sql
select now() AS now
FROM ignoreMe
```

| now   |
| ------------- |
| 1639150454255 |

This function is typically used in predicate to filter on timestamp for recent data.
e.g. filter data on recent 1 day(86400 seconds)

```sql
SELECT * 
FROM tableName
WHERE tsInMillis > now() - 86400000
```
