---
description: This section contains reference documentation for the substr function.
---

# substr

Get substring of the input string from start to endIndex.
Index begins at 0.
Set endIndex to -1 to calculate till end of the string

## Signature

> SUBSTR(col, startIndex, endIndex)

## Usage Examples

```sql
select SUBSTR('Pinot', 1, -1) AS name
FROM ignoreMe
```

| name   |
| ------------- |
| inot |

```sql
select SUBSTR('Pinot', 0, 2) AS name
FROM ignoreMe
```

| name   |
| ------------- |
| Pi |
