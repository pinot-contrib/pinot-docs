---
description: This section contains reference documentation for the FLOOR function.
---

# FLOOR

Rounded down to the nearest integer.

## Signature

> FLOOR(col1)

## Usage Examples

```sql
select FLOOR(12.1) AS value
from ignoreMe
```

| value |
| ----- |
| 12    |

```sql
select FLOOR(-12.1) AS value
from ignoreMe
```

| value |
| ----- |
| -13   |
