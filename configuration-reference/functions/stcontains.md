---
description: This section contains reference documentation for the ST_Contains function.
---

# ST_Contains

Returns true if and only if no points of the second geometry/geography lie in the exterior of the first geometry/geography, and at least one point of the interior of the first geometry lies in the interior of the second geometry.

## Signature

> ST_Contains(geometry/geography, geometry/geography)

## Warning
ST_Contains on Geography only give close approximation.

## Usage Examples

These examples are based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select group_city, 
       ST_AsText(location) AS locationString,  
       ST_Contains(
         ST_GeomFromText('POLYGON ((
             -74.171737 40.607377, 
             -74.089339 40.753180, 
             -73.911498 40.769303, 
             -74.016555 40.604249,  
             -74.171737 40.607377))'),
	       toGeometry(location)
	     ) AS inPolygon
from meetupRsvp 
order by inPolygon DESC
limit 5
```

| group_city | locationString | inPolygon |
| ------------- | ------------- | ------------- |
|New York	|POINT (-73.99 40.75)|	1|
|New York	|POINT (-73.99 40.75)|	1|
|Staten Island	|POINT (-74.15 40.61)|	1|
|New York	|POINT (-73.99 40.75)|	1|
|New York	|POINT (-73.99 40.75)|	1|


```sql
select count(*)
from meetupRsvp
WHERE ST_Contains(
         ST_GeomFromText('POLYGON ((
             -74.171737 40.607377, 
             -74.089339 40.753180, 
             -73.911498 40.769303, 
             -74.016555 40.604249,  
             -74.171737 40.607377))'),
	       toGeometry(location)
	     ) = 1
```

| count(*) |
| -------------  |
| 8 |