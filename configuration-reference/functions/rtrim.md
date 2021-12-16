---
description: This section contains reference documentation for the rtrim function.
---

# rtrim

rtrim spaces from right side of the string

## Signature

> RTRIM(col)

## Usage Examples

```sql
SELECT ' Pinot with spaces  ' AS notTrimmed,
       rtrim(' Pinot with spaces ') AS trimmed
FROM ignoreMe
```

| notTrimmed   | trimmed | 
| ------------- | ------------- |
| `" Pinot with spaces  "` | `" Pinot with spaces"` | 
