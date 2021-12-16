---
description: This section contains reference documentation for the STRPOS function.
---

# STRPOS

Find Nth instance of find string in input.
Returns 0 if input string is empty. Returns -1 if the Nth instance is not found or input string is null.

## Signature

> STRPOS(col, find, N)

## Usage Examples

```sql
SELECT STRPOS('Apache Pinot is a column-oriented, open-source, distributed data store written in Java', 'o', 1) AS value
FROM ignoreMe
```

| value   | 
| ------------- |
| 10 |


```sql
SELECT STRPOS('Apache Pinot is a column-oriented, open-source, distributed data store written in Java', 'o', 2) AS value
FROM ignoreMe
```

| value   | 
| ------------- |
| 19 |

```sql
SELECT STRPOS('Apache Pinot is a column-oriented, open-source, distributed data store written in Java', 'z', 1) AS value
FROM ignoreMe
```

| value   | 
| ------------- |
| -1 |