---
description: This section contains reference documentation for the ST_GeomFromWKB function.
---

# ST_GeomFromWKB

Returns a geometry type object from WKB representation.

## Signature

> ST_GeomFromWKB(wkb)

## Usage Examples

```sql
select STPOINT(-122, 37) AS point,
       ST_GeomFromWKB(
         ST_AsBinary(STPOINT(-122, 37))
       ) AS value
from ignoreMe 
```

| point | value   | 
| ------------- | ------------- |
| 00c05e8000000000004042800000000000 | 00c05e8000000000004042800000000000 |

{% hint style="info" %}
You can create geometry objects in the WKB format using the [ST_AsBinary](stasbinary.md) function.
{% endhint %}