---
description: This section contains reference documentation for the minString function.
---

# minString

Get the minimum string value lexicographically from a string column

## Signature

> MINSTRING(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select MINSTRING(playerName) as minString from baseballStats
```

| minString |
|-----------|
| A. Harry  |
