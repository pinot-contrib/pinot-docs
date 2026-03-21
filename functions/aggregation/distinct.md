---
description: This section contains reference documentation for the DISTINCT function.
---

# DISTINCT

Returns the distinct row values in a group

## Signature

> DISTINCT(colName)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCT league AS value
from baseballStats 
```

| value |
| ----- |
| NL    |
| UA    |
| AL    |
| NA    |
| PL    |
| AA    |
| FL    |

```sql
select DISTINCT(league) AS value
from baseballStats 
```

| value |
| ----- |
| NL    |
| UA    |
| AL    |
| NA    |
| PL    |
| AA    |
| FL    |
