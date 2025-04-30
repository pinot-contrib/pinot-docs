---
description: This section contains reference documentation for the remove function.
---

# remove

Removes all instances of search from string

## Signature

> remove(input, search)

## Usage Examples

```sql
select remove('foo bar foo sheep', 'foo') AS value
from ignoreMe
```

| value     |
| --------- |
| bar sheep |
