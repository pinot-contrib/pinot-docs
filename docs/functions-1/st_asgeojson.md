---
description: This section contains reference documentation for the ST_AsGeoJSON function.
---

# ST\_AsGeoJSON

Returns the [GeoJSON](https://datatracker.ietf.org/doc/html/rfc7946) representation of the given geometry or geography.

## Signature

> ST\_AsGeoJSON(geometryObject)

<table><thead><tr><th width="232">Arguments</th><th>Description</th></tr></thead><tbody><tr><td>geometryObject</td><td>A geometry or geography object.</td></tr></tbody></table>

## Usage Examples

```sql
select stAsGeoJSON( STPOINT(-122, 37) ) AS value
from ignoreMe
```

| value                                                                                           |
| ----------------------------------------------------------------------------------------------- |
| {"type":"Point","coordinates":\[-122,37],"crs":{"type":"name","properties":{"name":"EPSG:0"\}}} |



```sql
select stAsGeoJSON( ST_GeogFromText('LINESTRING (30 10, 10 30, 40 40)') ) AS value
from ignoreMe 
```

| value                                                                                                                      |
| -------------------------------------------------------------------------------------------------------------------------- |
| {"type":"LineString","coordinates":\[\[30,10],\[10,30],\[40,40]],"crs":{"type":"name","properties":{"name":"EPSG:4326"\}}} |

