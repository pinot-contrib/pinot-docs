---
description: This section contains reference documentation for the Extract function.
---

# Extract

Returns the selected field from the DATETIME expression.

### Signature

> EXTRACT(field FROM expression)

### Usage Examples

```sql
select EXTRACT(MONTH FROM '2017-06-15')
```

| value |
| ----- |
| 06    |

```sql
select EXTRACT(YEAR FROM '2017-06-15 09:34:21')
```

| value |
| ----- |
| 2017  |
