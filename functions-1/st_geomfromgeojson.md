---
description: >-
  This section contains reference documentation for the ST_GeomFromGeoJSON
  function.
---

# ST\_GeomFromGeoJSON

Returns a geometry type object from  [GeoJSON ](https://datatracker.ietf.org/doc/html/rfc7946) representation, with the optional spatial system reference.

## Signature

> ST\_GeomFromGeoJSON(geoJSON)

## Usage Examples

```sql
select ST_GeomFromGeoJSON(
'{ "type": "Point", "coordinates": [100.0, 0.0] }'
) AS value
from ignoreMe 
```

| value                              |
| ---------------------------------- |
| 0040590000000000000000000000000000 |



```sql
select ST_GeomFromGeoJSON(
'{
     "type": "LineString",
     "coordinates": [
         [100.0, 0.0],
         [101.0, 1.0]
     ]
 }') AS value
from ignoreMe 
```

| value                                                                                      |
| ------------------------------------------------------------------------------------------ |
| 020000000100000002000000004059000000000000000000000000000040594000000000003ff0000000000000 |



```sql
select ST_GeomFromGeoJSON(
'{
   "type": "Polygon",
   "coordinates": [
       [
           [100.0, 0.0],
           [101.0, 0.0],
           [101.0, 1.0],
           [100.0, 1.0],
           [100.0, 0.0]
       ]
   ]
}') AS value
from ignoreMe 
```

| value                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 040000000100000005000000004059000000000000000000000000000040590000000000003ff000000000000040594000000000003ff00000000000004059400000000000000000000000000040590000000000000000000000000000 |

