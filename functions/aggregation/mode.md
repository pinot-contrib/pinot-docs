---
description: This section contains reference documentation for the mode function.
---

# mode

Get the most frequent value in a group. When multiple modes are present it gives the minimum of all the modes. This behavior can be overridden to get the maximum or the average mode.

## Signature

> MODE(colName, \[reducerType], \[dataType])

* `reducerType` (optional): how to break ties when multiple modes are present. One of `MIN` (default), `MAX`, or `AVG`.
* `dataType` (optional): one of `STRING`, `BOOLEAN`, or `TIMESTAMP`. It is also the result type, and the input expression must have a matching stored type. Only the `MIN` and `MAX` reducers are supported for these types (`AVG` is rejected). When `dataType` is omitted, the input expression must be numeric and the result is a `DOUBLE`.

`MODE` also works directly on `STRING` columns (including JSON columns read as strings) without the `dataType` argument: `MODE(stringCol)` returns a `STRING`, and `MIN`/`MAX` break ties lexicographically (default `MIN`).

Typed `BOOLEAN` and `TIMESTAMP` results are opt-in through the explicit three-argument form, for example `MODE(boolCol, 'MIN', 'BOOLEAN')` or `MODE(tsCol, 'MAX', 'TIMESTAMP')`. Existing one- and two-argument calls over numeric columns keep their `DOUBLE` results and `AVG` support.

{% hint style="info" %}
The explicit three-argument form requires servers that support typed `MODE`. During a rolling upgrade, older servers reject `MODE(col, reducer, dataType)`, while existing one- and two-argument calls continue to work.
{% endhint %}

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch-processing).

```sql
select mode(yearID) AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001
```

| value |
| ----- |
| 2008  |

```sql
select mode(yearID, 'AVG') AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001
```

| value |
| ----- |
| 2010  |

```sql
select mode(yearID, 'MIN') AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001
```

| value |
| ----- |
| 2008  |

```sql
select mode(yearID, 'MAX') AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001
```

| value |
| ----- |
| 2012  |
