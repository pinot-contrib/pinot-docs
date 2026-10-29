---
description: This section contains reference documentation for the ARRAYAGG function.
---

# ARRAYAGG

Aggregates values from rows into an array. Supports collecting values of type `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `BOOLEAN`, `TIMESTAMP`, `STRING`, `JSON`, `BYTES`, and `UUID`. Use the optional `DISTINCT` keyword to collect only distinct values.

## Signature

> ARRAYAGG(colName)
>
> ARRAYAGG(DISTINCT colName)
>
> ARRAYAGG(colName, 'dataType')
>
> ARRAYAGG(colName, 'dataType', 'DISTINCT')

The `dataType` argument is optional. When it is omitted, Pinot infers it from the type of `colName` (the element type for a multi-value column); a `JSON` column is collected as `STRING`. If the inferred or supplied type is not supported, the query fails in the broker.

When provided, the `dataType` parameter must be one of: `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `BOOLEAN`, `TIMESTAMP`, `STRING`, `JSON`, `BYTES`, or `UUID`. `JSON` values are collected as strings, and `UUID` values are returned in canonical UUID string form.

Distinct values can be collected either with the `DISTINCT` keyword inside the call (`ARRAYAGG(DISTINCT colName)`) or by passing `'DISTINCT'` as the trailing argument of the explicit-type form.

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

The `dataType` argument can be omitted; Pinot infers it from the column type:

```sql
select ARRAYAGG(yearID) AS years
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

The `DISTINCT` keyword inside the call collects distinct values without an explicit `dataType`:

```sql
select ARRAYAGG(DISTINCT league) AS leagues
from baseballStats
WHERE playerName = 'Barry Bonds'
```

| leagues      |
| ------------ |
| [NL, AL]     |

When the input column is multi-value, Pinot flattens each row's values into the output array before applying the optional distinct step.
