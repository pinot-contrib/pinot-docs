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

### WITHIN GROUP clause

Use the `WITHIN GROUP (ORDER BY ...)` clause to control the order of values in the concatenated result. Without this clause the order of values is undefined.

> LISTAGG(colName, delimiter) WITHIN GROUP (ORDER BY sortCol)
>
> LISTAGG(DISTINCT colName, delimiter) WITHIN GROUP (ORDER BY sortCol)

{% hint style="info" %}
The `WITHIN GROUP` clause requires the **multi-stage query engine** (v2). It was introduced in Apache Pinot 1.2.0 ([#13146](https://github.com/apache/pinot/pull/13146)).

Only a single `WITHIN GROUP` clause is supported per query.
{% endhint %}

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

**Basic aggregation**

```sql
select LISTAGG(league, '/') AS value
from baseballStats
WHERE playerName = 'Barry Bonds'
```

| value                               |
| ----------------------------------- |
| NL/NL/NL/NL/NL/NL/NL/NL/NL/NL/... |

**Distinct values**

```sql
select LISTAGG(DISTINCT league, ', ') AS value
from baseballStats
WHERE playerName = 'Barry Bonds'
```

| value  |
| ------ |
| NL, AL |

**Ordered aggregation with WITHIN GROUP**

Concatenate carriers in alphabetical order for each origin–destination pair:

```sql
SELECT Origin, Dest,
  LISTAGG(DISTINCT Carrier, ', ') WITHIN GROUP (ORDER BY Carrier) AS carriers
FROM airlineStats
GROUP BY Origin, Dest
```

| Origin | Dest | carriers      |
| ------ | ---- | ------------- |
| SFO    | LAX  | AA, DL, UA, … |
| JFK    | BOS  | B6, DL, …     |

**Ordered aggregation with GROUP BY**

```sql
SELECT teamID,
  LISTAGG(playerName, ' | ') WITHIN GROUP (ORDER BY playerName) AS players
FROM baseballStats
GROUP BY teamID
```

| teamID | players                              |
| ------ | ------------------------------------ |
| PIT    | Barry Bonds \| Bobby Bonilla \| …    |
