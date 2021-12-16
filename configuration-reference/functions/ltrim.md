---
description: This section contains reference documentation for the ltrim function.
---

# ltrim

trim spaces from left side of the string

## Signature

> LTRIM(col)

## Usage Examples

```sql
SELECT ' Pinot with spaces  ' AS notTrimmed,
       ltrim(' Pinot with spaces ') AS trimmed
FROM ignoreMe
```

| notTrimmed   | trimmed | 
| ------------- | ------------- |
| `" Pinot with spaces  "` | `"Pinot with spaces "` | 
