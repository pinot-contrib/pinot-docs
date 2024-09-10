---
description: This section contains reference documentation for the CODEPOINT function.
---

# codepoint

the Unicode codepoint of the first character of the string

## Signature

> CODEPOINT(col)

## Usage Examples

```sql
SELECT CODEPOINT('Apache Pinot') AS value
FROM ignoreMe
```

| value |
| ----- |
| 65    |
