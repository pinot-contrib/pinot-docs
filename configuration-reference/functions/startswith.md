---
description: This section contains reference documentation for the STARTSWITH function.
---

# STARTSWITH

returns true if columns starts with prefix string.

## Signature

> STARTSWITH(col, prefix)

## Usage Examples

```sql
SELECT STARTSWITH('Apache Pinot', 'Apache') AS value
FROM ignoreMe
```

| value   | 
| ------------- |
| true |


```sql
SELECT STARTSWITH('Apache Pinot', 'Pinot') AS value
FROM ignoreMe
```

| value   | 
| ------------- |
| false |
