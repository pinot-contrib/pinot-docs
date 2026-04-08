---
description: >-
  This section contains reference documentation for the FIRST_VALUE window
  function.
---

# FIRST\_VALUE

The `FIRST_VALUE` function returns the value from the first row in a window.&#x20;

### Signature

```sql
FIRST_VALUE(expression) [IGNORE NULLS | RESPECT NULLS] OVER ()
```

The default behavior is `RESPECT NULLS`. If the `IGNORE NULLS` option is specified, the function returns the first non-null row in each window (assuming one exists, `null` otherwise).

### Example

This example computes the number of games played by a player in their first year.

```sql
SELECT playerName,
  yearID,
  numberOfGames,
  FIRST_VALUE(numberOfGames) OVER (
    PARTITION BY playerName
    ORDER BY yearID ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
  )
FROM baseballStats;
```

Output:

| playerName | yearID | numberOfGames | EXPR$3 |
| --- | --- | --- | --- |
| p1 | 2000 | 10 | 10 |
| p1 | 2001 | 15 | 10 |
| p1 | 2002 | 12 | 10 |
| p2 | 1990 | 120 | 120 |
| p2 | 1991 | 124 | 120 |
| p3 | 2006 | 30 | 30 |
| p3 | 2007 | 25 | 30 |
| p3 | 2009 | 20 | 30 |
| p3 | 2010 | 15 | 30 |
