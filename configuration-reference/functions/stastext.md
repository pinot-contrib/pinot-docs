---
description: This section contains reference documentation for the ST_AsText function.
---

# ST\_AsText

Returns the WKT representation of the geometry/geography.

## Signature

> ST\_AsText(geometryObject)

## Usage Examples

```sql
select stAsText(
    STPOINT(-122, 37)
) AS value
from ignoreMe 
```

| value           |
| --------------- |
| POINT (-122 37) |

```sql
select stAsText(
    ST_GeogFromText('LINESTRING (30 10, 10 30, 40 40)')
) AS value
from ignoreMe 
```

| value                            |
| -------------------------------- |
| LINESTRING (30 10, 10 30, 40 40) |
