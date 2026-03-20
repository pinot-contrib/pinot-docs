---
description: This section contains reference documentation for the maxString function.
---

# maxString

Get the maximum string value lexicographically from a string column

## Signature

> MAXSTRING(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../basics/getting-started/quick-start.md#batch).

```sql
select MAXSTRING(playerName) as maxString from baseballStats
```

| maxString      |
|----------------|
| Zoilo Casanova |
