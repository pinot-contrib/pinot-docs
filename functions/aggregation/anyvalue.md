---
description: This section contains reference documentation for the ANYVALUE function.
---

# ANYVALUE

Returns any arbitrary non-null value from the column for each group. Useful in GROUP BY queries for including columns that have a one-to-one mapping with the GROUP BY columns without adding them to the GROUP BY clause.

## Signature

> ANYVALUE(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select league, ANYVALUE(playerName) AS samplePlayer
from baseballStats
GROUP BY league
```

| league | samplePlayer |
| ------ | ------------ |
| AA     | David Orr    |
| NL     | Fred Pfeffer |
