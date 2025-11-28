---
description: This section contains reference documentation for the trim function.
---

# trim

trim spaces from both side of the string

## Signature

> TRIM(col)

## Usage Examples

```sql
SELECT ' Pinot with spaces  ' AS notTrimmed,
       trim(' Pinot with spaces ') AS trimmed
FROM ignoreMe
```

| notTrimmed              | trimmed               |
| ----------------------- | --------------------- |
| `" Pinot with spaces "` | `"Pinot with spaces"` |
