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

<table><thead><tr><th>playerName</th><th>yearID</th><th>numberOfGames</th><th data-type="number">EXPR$3</th></tr></thead><tbody><tr><td>p1</td><td>2000</td><td>10</td><td>10</td></tr><tr><td>p1</td><td>2001</td><td>15</td><td>10</td></tr><tr><td>p1</td><td>2002</td><td>12</td><td>10</td></tr><tr><td>p2</td><td>1990</td><td>120</td><td>120</td></tr><tr><td>p2</td><td>1991</td><td>124</td><td>120</td></tr><tr><td>p3</td><td>2006</td><td>30</td><td>30</td></tr><tr><td>p3</td><td>2007</td><td>25</td><td>30</td></tr><tr><td>p3</td><td>2009</td><td>20</td><td>30</td></tr><tr><td>p3</td><td>2010</td><td>15</td><td>30</td></tr></tbody></table>
