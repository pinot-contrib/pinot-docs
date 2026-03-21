---
description: This section contains reference documentation for the BOOLAND function.
---

# BOOLAND

Returns the logical AND of all boolean values in a group. Returns `true` only if every value in the group is `true`; returns `false` if any value is `false`. When no records are selected, the default value is `true` (the identity element for AND).

## Signature

> BOOLAND(colName)

## Usage Examples

```sql
select BOOLAND(isActive) AS value
from myTable
```

| value |
| ----- |
| false |

```sql
select city, BOOLAND(isActive) AS allActive
from myTable
GROUP BY city
```

| city         | allActive |
| ------------ | --------- |
| San Francisco | true      |
| New York     | false     |
