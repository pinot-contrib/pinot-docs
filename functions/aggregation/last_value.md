---
description: >-
  This section contains reference documentation for the LAST_VALUE window
  function.
---

# LAST\_VALUE

The `LAST_VALUE` function returns the value from the last row in a window.&#x20;

### Signature

```sql
LAST_VALUE(expression) [IGNORE NULLS | RESPECT NULLS] OVER ()
```

The default behavior is `RESPECT NULLS`. If the `IGNORE NULLS` option is specified, the function returns the last non-null row in each window (assuming one exists, `null` otherwise).



### Example 1

This example computes the number of games played by a player in their last year.

```sql
SELECT playerName,
  yearID,
  numberOfGames,
  LAST_VALUE(numberOfGames) OVER (
    PARTITION BY playerName
    ORDER BY yearID ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
FROM baseballStats;
```

Output:

| playerName | yearID | numberOfGames | EXPR$3 |
| --- | --- | --- | --- |
| p1 | 2000 | 10 | 12 |
| p1 | 2001 | 15 | 12 |
| p1 | 2002 | 12 | 12 |
| p2 | 1990 | 120 | 124 |
| p2 | 1991 | 124 | 124 |
| p3 | 2006 | 30 | 15 |
| p3 | 2007 | 25 | 15 |
| p3 | 2009 | 20 | 15 |
| p3 | 2010 | 15 | 15 |



### Example 2

This example uses the `IGNORE NULLS` option to "gapfill" missing values (that are represented as `null`). Note that we use the default window frame here which is `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

```sql
SELECT ts,
  reading,
  LAST_VALUE(reading) IGNORE NULLS OVER (
    ORDER BY ts
  ) AS imputedReading
FROM telemetryData;
```

Output:

| ts                    | reading | imputedReading |
| --------------------- | ------- | -------------- |
| 2014-01-01 00:00:00.0 | 10.0    | 10.0           |
| 2014-01-01 00:30:00.0 | 12.0    | 12.0           |
| 2014-01-01 01:00:00.0 | 12.5    | 12.5           |
| 2014-01-01 01:30:00.0 | null    | 12.5           |
| 2014-01-01 02:00:00.0 | null    | 12.5           |
| 2014-01-01 02:30:00.0 | 11.5    | 11.5           |
| 2014-01-01 03:00:00.0 | null    | 11.5           |
| 2014-01-01 03:30:00.0 | 11.0    | 11.0           |
