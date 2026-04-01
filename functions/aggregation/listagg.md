---
description: This section contains reference documentation for the LISTAGG function.
---

# LISTAGG

Aggregates string values from rows into a single delimited string. An optional delimiter can be specified (defaults to comma). Use the optional `DISTINCT` keyword to include only distinct values.

## Signature

> LISTAGG(colName)
>
> LISTAGG(colName, delimiter)
>
> LISTAGG(DISTINCT colName, delimiter)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select LISTAGG(league, '/') AS value
from baseballStats
WHERE playerName = 'Barry Bonds'
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>NL/NL/NL/NL/NL/NL/NL/NL/NL/NL/...</td>
    </tr>
  </tbody>
</table>

```sql
select LISTAGG(DISTINCT league, ', ') AS value
from baseballStats
WHERE playerName = 'Barry Bonds'
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>NL, AL</td>
    </tr>
  </tbody>
</table>
