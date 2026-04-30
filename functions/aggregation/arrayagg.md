---
description: This section contains reference documentation for the ARRAYAGG function.
---

# ARRAYAGG

Aggregates values from rows into an array. Supports collecting values of type `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `STRING`, and `BYTES`. Use the optional `DISTINCT` keyword to collect only distinct values.

## Signature

> ARRAYAGG(colName, 'dataType')
>
> ARRAYAGG(colName, 'dataType', 'DISTINCT')

The `dataType` parameter must be one of: `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `STRING`, or `BYTES`.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select ARRAYAGG(yearID, 'INT') AS years
from baseballStats
WHERE playerName = 'Barry Bonds'
```

| years                                                          |
| -------------------------------------------------------------- |
| [1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, ...] |

```sql
select ARRAYAGG(league, 'STRING', 'DISTINCT') AS leagues
from baseballStats
WHERE playerName = 'Barry Bonds'
```

| leagues      |
| ------------ |
| [NL, AL]     |

When the input column is multi-value, Pinot flattens each row's values into the output array before applying the optional distinct step.
