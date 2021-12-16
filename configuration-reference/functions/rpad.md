---
description: This section contains reference documentation for the RPAD function.
---

# RPAD

string padded from the right side with `pad` to reach final `size`

## Signature

> RPAD(col, size, pad)

## Usage Examples

```sql
SELECT RPAD('Hello, World', '20', '*') AS value
FROM ignoreMe
```

| value   | 
| ------------- |
| Hello, World******** |