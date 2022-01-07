---
description: This section contains reference documentation for the ST_POINT/STPOINT function.
---

# STPOINT

Returns a geometry or geography type point object with the given coordinate values.

## Signature

> STPOINT(x, y)
>
> STPOINT(x, y, isGeography)
>
> ST_POINT(x, y)
>
> ST_POINT(x, y, isGeography)

## Usage Examples

```sql
select STPOINT(-122, 37) AS value
from ignoreMe 
```

| value   | 
| ------------- |
| 00c05e8000000000004042800000000000 |

```sql
select STPOINT(-122, 37, 0) AS value
from ignoreMe 
```

| value   | 
| ------------- |
| 00c05e8000000000004042800000000000 |

```sql
select STPOINT(-122, 37, 1) AS value
from ignoreMe 
```

| value   | 
| ------------- |
| 80c05e8000000000004042800000000000 |


```sql
select ST_POINT(-122, 37, 1) AS value
from ignoreMe 
```

| value   | 
| ------------- |
| 80c05e8000000000004042800000000000 |
