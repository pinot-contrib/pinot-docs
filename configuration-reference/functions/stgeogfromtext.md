---
description: >-
  This section contains reference documentation for the ST_GeogFromText
  function.
---

# ST\_GeogFromText

Return a specified geography value from [Well-Known Text representation or extended (WKT)](https://en.wikipedia.org/wiki/Well-known\_text\_representation\_of\_geometry)

## Signature

> ST\_GeogFromText(wkt)

## Usage Examples

```sql
select ST_GeogFromText('POINT (30 10)') AS value
from ignoreMe 
```

| value                              |
| ---------------------------------- |
| 80403e0000000000004024000000000000 |

```sql
select ST_GeogFromText('LINESTRING (30 10, 10 30, 40 40)') AS value
from ignoreMe 
```

| value                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------- |
| 82000000010000000300000000403e00000000000040240000000000004024000000000000403e00000000000040440000000000004044000000000000 |

```sql
select ST_GeogFromText('POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))') AS value
from ignoreMe 
```

| value                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 84000000010000000500000000403e0000000000004024000000000000402400000000000040340000000000004034000000000000404400000000000040440000000000004044000000000000403e0000000000004024000000000000 |
