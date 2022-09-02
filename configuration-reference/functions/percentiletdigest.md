---
description: >-
  This section contains reference documentation for the PERCENTILETDigest
  function.
---

# percentiletdigest

Returns the Nth percentile of the group using [T-digest algorithm](https://raw.githubusercontent.com/tdunning/t-digest/master/docs/t-digest-paper/histo.pdf).

## Signature

> PERCENTILETDigest(colName, percentile)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select PERCENTILETDigest(homeRuns, 50) AS value
from baseballStats 
```

| value |
| ----- |
| 0     |

```sql
select PERCENTILETDigest(homeRuns, 80) AS value
from baseballStats 
```

| value              |
| ------------------ |
| 3.6571905392487856 |

```sql
select PERCENTILETDigest(homeRuns, 99.9) AS value
from baseballStats 
```

| value             |
| ----------------- |
| 46.26787306220119 |
