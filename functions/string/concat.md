---
description: This section contains reference documentation for the concat function.
---

# concat

Concatenate two input strings using the separator

## Signature

> CONCAT(col1, col2, separator)

## Usage Examples

```sql
SELECT concat('Apache', 'Pinot', ' ') AS value
FROM ignoreMe
```

| value        |
| ------------ |
| Apache Pinot |

```sql
SELECT concat('real-time', 'analytics', '__') AS value
FROM ignoreMe
```

| value                  |
| ---------------------- |
| real-time\_\_analytics |
