---
description: This section contains reference documentation for the BOOLOR function.
---

# BOOLOR

Returns the logical OR of all boolean values in a group. Returns `true` if any value in the group is `true`; returns `false` only if every value is `false`. When no records are selected, the default value is `false` (the identity element for OR).

## Signature

> BOOLOR(colName)

## Usage Examples

```sql
select BOOLOR(hasError) AS value
from myTable
```

| value |
| ----- |
| true  |

```sql
select city, BOOLOR(hasError) AS anyErrors
from myTable
GROUP BY city
```

| city         | anyErrors |
| ------------ | --------- |
| San Francisco | true      |
| New York     | false     |
