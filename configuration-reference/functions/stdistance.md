---
description: This section contains reference documentation for the ST_Distance function.
---

# ST_Distance

For geometry type, returns the 2-dimensional cartesian minimum distance (based on spatial ref) between two geometries in projected units. For geography, returns the great-circle distance in meters between two SphericalGeography points. Note that g1, g2 shall have the same type.

## Signature

> ST_Distance(geography/geometry, geography/geometry)

## Usage Examples

These examples are based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select group_city, 
       STASTEXT(location) AS locationString, 
	   ST_Distance(location, ST_POINT(2.154007,41.390205, 1)) AS distanceInMetres
from meetupRsvp 
LIMIT 1
```

| group_city   | locationString | distanceInMetres | 
| ------------- | -------------  | -------------  | 
|Madrid | POINT (-3.71 40.42) | 504376.5534398629  | 
