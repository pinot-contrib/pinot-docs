---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTBITMAP
  function.
---

# DISTINCTCOUNTBITMAP

Returns the count of distinct row values in a group. This function is accurate for _INT_ column, but approximate for other cases where hash codes are used in distinct counting and there may be hash collisions.\
For accurate distinct counting on all column types, see [DISTINCTCOUNT](distinctcount.md).

## Signature

> DISTINCTCOUNTBITMAP(colName)

With [advanced null handling](../../build-with-pinot/querying-and-sql/null-value-support.md#advanced-null-handling-support) enabled, Pinot skips null rows. Without advanced null handling, the column's configured default null value contributes to the bitmap. The function returns `0` when no non-null rows contribute.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select DISTINCTCOUNTBITMAP(league) AS value
from baseballStats 
```

| value |
| ----- |
| 7     |

```sql
select DISTINCTCOUNTBITMAP(teamID) AS value
from baseballStats 
```

| value |
| ----- |
| 148   |
