---
description: This section contains reference documentation for the ARRAYAGG function.
---

# ARRAYAGG

Aggregates values from rows into an array. Supports collecting values of type INT, LONG, FLOAT, DOUBLE, and STRING. Use the optional `DISTINCT` keyword to collect only distinct values.

## Signature

> ARRAYAGG(colName, 'dataType')
>
> ARRAYAGG(colName, 'dataType', 'DISTINCT')

The `dataType` parameter must be one of: `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select ARRAYAGG(yearID, 'INT') AS years
from baseballStats
WHERE playerName = 'Barry Bonds'
```

<table>
  <thead>
    <tr>
      <th>years</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, ...]</td>
    </tr>
  </tbody>
</table>

```sql
select ARRAYAGG(league, 'STRING', 'DISTINCT') AS leagues
from baseballStats
WHERE playerName = 'Barry Bonds'
```

<table>
  <thead>
    <tr>
      <th>leagues</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[NL, AL]</td>
    </tr>
  </tbody>
</table>
