---
description: This section contains reference documentation for the ST_GeogFromWKB function.
---

# ST_GeogFromWKB

Returns a geography type object from WKB representation.

## Signature

> ST_GeogFromWKB(wkb)

## Usage Examples

```sql
select STPOINT(-122, 37) AS point,
       ST_GeogFromWKB(
         ST_AsBinary(STPOINT(-122, 37))
       ) AS value
from ignoreMe 
```

| point | value   | 
| ------------- | ------------- |
| 00c05e8000000000004042800000000000 | 80c05e8000000000004042800000000000 |

```sql
select STPOINT(-122, 37, 1) AS point,
       ST_GeogFromWKB(
         ST_AsBinary(STPOINT(-122, 37, 1))
       ) AS value
from ignoreMe 
```

| point | value   | 
| ------------- | ------------- |
| 80c05e8000000000004042800000000000 | 80c05e8000000000004042800000000000 |


{% hint style="info" %}
You can create geometry objects in the WKB format using the [ST_AsBinary](stasbinary.md) function.
{% endhint %}