---
description: This section contains reference documentation for the LPAD function.
---

# lpad

string padded from the left side with `pad` to reach final `size`

## Signature

> LPAD(col, size, pad)

## Usage Examples

```sql
SELECT LPAD('Hello, World', '20', '*') AS value
FROM ignoreMe
```

| value                        |
| ---------------------------- |
| \*\*\*\*\*\*\*\*Hello, World |
