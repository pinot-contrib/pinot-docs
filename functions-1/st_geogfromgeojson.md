---
description: >-
  This section contains reference documentation for the ST_GeogFromGeoJSON
  function.
---

# ST\_GeogFromGeoJSON

Return a specified geography value from [GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946) representation.

## Signature

> ST\_GeogFromGeoJSON(geoJSON)

## Usage Examples

```sql
select ST_GeogFromGeoJSON(
'{ "type": "Point", "coordinates": [100.0, 0.0] }'
) AS value
from ignoreMe 
```

| value                              |
| ---------------------------------- |
| 8040590000000000000000000000000000 |



```sql
select ST_GeogFromGeoJSON(
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
| 820000000100000002000000004059000000000000000000000000000040594000000000003ff0000000000000 |



```sql
select ST_GeogFromGeoJSON(
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
| 840000000100000005000000004059000000000000000000000000000040590000000000003ff000000000000040594000000000003ff00000000000004059400000000000000000000000000040590000000000000000000000000000 |



