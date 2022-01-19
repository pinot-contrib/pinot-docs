---
description: This section contains reference documentation for the remove function.
---

# regexpExtract

Extracts values that match the provided regular expression

## Signature

> remove(input, search)

## Usage Examples

```sql
select remove('foo bar foo sheep', 'foo') AS value
from ignoreMe
```

| value   | 
| ------------- |
| bar sheep |
